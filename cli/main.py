import os
import sys
import time
import re
from datetime import datetime

import openai
from colorama import Fore
from colorama import Style
from colorama import init as colorama_init
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style as PromptStyle

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cli import __version__
from cli.core import ensure_api_key, icase_contains, chatgpt_response, check_args_for_key, get_env


def main():
    """
    chatgpt-cli [api_key] [out_file]
    """

    key_in_args, file_out = check_args_for_key()

    openai.api_key = ensure_api_key(prompt=True, use_args_key=key_in_args)

    history_size = int(get_env('HISTORY_SIZE', '3'))

    text_width = int(get_env('CHAT_TEXT_WIDTH', '0'))

    colored = icase_contains(get_env('CHAT_COLORED', 'true'), ['true', 'yes', 'on'])
    color_you = get_env('CHAT_COLOR_YOU', 'green').upper()
    color_ai = get_env('CHAT_COLOR_AI', 'white').upper()

    if colored:
        colorama_init(autoreset=True)

        color_you_ansi = getattr(Fore, color_you) if color_you in Fore.__dict__.keys() and color_you != 'WHITE' else ''
        color_ai_ansi = getattr(Fore, color_ai) if color_ai in Fore.__dict__.keys() and color_ai != 'WHITE' else ''
        color_end = Style.RESET_ALL
    else:
        color_you_ansi = ''
        color_ai_ansi = ''
        color_end = ''

    print(f'Welcome to the ChatGPT command-line interface v{__version__}\n')
    print('Please enter your question (type "/quit" to stop chatting, type "/reset" to clear chat history)\n')

    file = None
    file_messages = []
    if file_out:
        file_dir = os.path.dirname(file_out)
        if file_dir != '' and not os.path.exists(file_dir):
            os.makedirs(file_dir, exist_ok=True)

        option = None
        if os.path.exists(file_out):
            print(
                f'Output file "{file_out}" already exists, please select one of the options:\n'
                '1. Continue conversation\n'
                '2. Keep previous content and start new conversation\n'
                '3. Delete previous content and start new conversation\n')
            while not option:
                answer = input('Selected option: ')
                try:
                    if not answer:
                        print('1')
                    option = int(answer if answer != '' else '1')
                    if option not in [1, 2, 3]:
                        option = None
                        raise ValueError('Invalid option')
                    else:
                        print('\n', end='')
                except ValueError:
                    print('Invalid option selected. Available options: 1, 2, or 3\n')

        file = open(file_out, 'w' if option == 3 else 'a')
        now = datetime.now()
        prefix = '\n\n' if os.path.getsize(file_out) > 0 else ''
        file.write(f'{prefix}[{now.isoformat()}]\n')
        file.flush()

        if option == 1:
            date_pattern = re.compile("^\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}]$")
            with open(file_out, 'r') as fp:
                role = None
                content = ''
                for line in fp:
                    line_text = line if not date_pattern.match(line) else ''
                    new_role = None
                    if line.startswith('AI: '):
                        new_role = 'assistant'
                        line_text = line.replace('AI: ', '', 1)
                    if line.startswith('You: '):
                        new_role = 'user'
                        line_text = line.replace('You: ', '', 1)
                    if role is None:
                        role = new_role

                    if role is not None:
                        content += line_text

                    if role != new_role and role is not None:
                        if not icase_contains(content.replace('\n', ''),
                                              ['/quit', '/q', '/reset', '/r', 'goodbye']) and \
                                content.replace('\n', '') != 'Let\'s start a new conversation.':
                            file_messages.append({'role': role, 'content': content})
                        role = new_role
                        content = ''

                    if icase_contains(line_text.replace('\n', ''), ['/reset', '/r']):
                        file_messages.clear()

    end = False
    chat_history = [*file_messages[-2 * (history_size + 1):]]
    while end is False:
        stream_content = ''
        stream_in_progress = False
        try:
            try:
                style = PromptStyle.from_dict(
                    {'': f'ansi{color_you.lower()}' if color_you_ansi != '' else ''})
                question = prompt('You: ', style=style)
            except Exception:
                question = input(f'{color_you_ansi}You: ')
                if colored:
                    print('', end=color_end)

            if file:
                file.write(f'\nYou: {question}\n')
                file.flush()

            if question is None or question.strip() == '':
                continue

            if icase_contains(question, ['/quit', '/q']):
                break

            if icase_contains(question, ['/reset', '/r']):
                chat_history = []
                print(f'\n{color_ai_ansi}AI: Let\'s start a new conversation.\n\n', end=color_end)
                if file:
                    file.write(f'\nAI: Let\'s start a new conversation.\n\n')
                    file.flush()
                continue

            message = {'role': 'user', 'content': question}
            messages = [
                *chat_history,
                message
            ]

            response = chatgpt_response(messages)
            if response is None:
                break

            if file and isinstance(response, str):
                file.write(f'\nAI: {response}\n')
                file.flush()

            chat_history.append(message)

            if isinstance(response, str):
                chat_history.append({'role': 'assistant', 'content': response})
            else:
                stream_in_progress = True

            print(f'\n{color_ai_ansi}AI: ', end=color_end)
            count = 0
            for token in response:
                for char in token:
                    count += 1
                    stream_content += char
                    print(f'{color_ai_ansi}{char}', end=color_end, flush=True)
                    if 0 < text_width <= count:
                        print('')
                        count = 0
                    time.sleep(0.01)
            print('\n')
            stream_in_progress = False

            if not isinstance(response, str):
                chat_history.append({'role': 'assistant', 'content': stream_content})
                if file:
                    file.write(f'\nAI: {stream_content}\n')
                    file.flush()

            if len(chat_history) >= (history_size + 1) * 2:
                chat_history = chat_history[2:]
        except KeyboardInterrupt:
            if stream_in_progress:
                chat_history.append({'role': 'assistant', 'content': stream_content})
                if file:
                    file.write(f'\nAI: {stream_content}\n')
                    file.flush()
                print('\n')
            else:
                break
    print(f'\n{color_ai_ansi}AI: Goodbye', end=color_end)
    if file:
        file.write(f'\nAI: Goodbye\n')
        file.close()


if __name__ == '__main__':
    main()
