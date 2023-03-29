import time

import openai
from colorama import Fore
from colorama import Style
from colorama import init as colorama_init

from cli.core import ensure_api_key, icase_contains, chatgpt_response, get_env


def main():
    """
    chatgpt-cli [api_key]
    """

    history_size = int(get_env('HISTORY_SIZE', '3'))

    text_width = int(get_env('CHAT_TEXT_WIDTH', '0'))

    openai.api_key = ensure_api_key(prompt=True)

    colored = icase_contains(get_env('CHAT_COLORED', 'true'), ['true', 'yes', 'on'])
    color_you = get_env('CHAT_COLOR_YOU', 'green').upper()
    color_ai = get_env('CHAT_COLOR_AI', 'white').upper()

    if colored:
        colorama_init(autoreset=True)

        color_you = getattr(Fore, color_you) if color_you in Fore.__dict__.keys() and color_you != 'WHITE' else ''
        color_ai = getattr(Fore, color_ai) if color_ai in Fore.__dict__.keys() and color_ai != 'WHITE' else ''
        color_end = Style.RESET_ALL
    else:
        color_you = ''
        color_ai = ''
        color_end = ''

    print(f'Welcome to the ChatGPT command-line interface\n')
    print('Please enter your question (type "exit" to stop chatting)\n')

    end = False
    chat_history = []
    while end is False:
        try:
            question = input(f'{color_you}You: ')

            if colored:
                print('', end=color_end)

            if question is None or question.strip() == '':
                continue

            if icase_contains(question, ['exit', 'quit', 'close', 'end']):
                break

            message = {'role': 'user', 'content': question}
            messages = [
                *chat_history,
                message
            ]

            response = chatgpt_response(messages)
            if response is None:
                break

            chat_history.append(message)
            chat_history.append({'role': 'assistant', 'content': response})
            if len(chat_history) >= (history_size + 1) * 2:
                chat_history = chat_history[2:]

            print(f'\n{color_ai}AI: ', end=color_end)
            count = 0
            for char in response:
                count += 1
                print(f'{color_ai}{char}', end=color_end, flush=True)
                if 0 < text_width <= count:
                    print('')
                    count = 0
                time.sleep(0.01)
            print('\n')
        except KeyboardInterrupt:
            break
    print(f'\n{color_ai}AI: Goodbye', end=color_end)


if __name__ == '__main__':
    main()
