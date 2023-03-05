import time

import openai

from cli.core import ensure_api_key, icase_contains, chatgpt_response


def main():
    """
    chatgpt-cli [api_key]
    """

    openai.api_key = ensure_api_key(prompt=True)

    print('Welcome to the ChatGPT command-line interface\n')
    print('Please enter your question (type "exit" to stop chatting)\n')

    end = False
    chat_history = []
    while end is False:
        try:
            question = input('You: ')

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
            if len(chat_history) > 4:
                chat_history.pop(0)

            print('\nAI: ', end='')
            for char in response:
                print(char, end='', flush=True)
                time.sleep(0.01)
            print('\n')
        except KeyboardInterrupt:
            break
    print('\nAI: Goodbye')


if __name__ == '__main__':
    main()
