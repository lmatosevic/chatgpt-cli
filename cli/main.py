import time

import openai

from cli.utils import find_api_key

model = 'gpt-3.5-turbo'


def main():
    openai.api_key = find_api_key(prompt=True)

    print('Welcome to the ChatGPT command line interface\n')
    print('Please enter your question (type "exit" to stop chatting)\n')

    end = False
    chat_history = []
    while end is False:
        try:
            question = input('You: ')

            if question is None or question.strip() == '':
                continue

            if question.strip().lower() in ['exit', 'quit', 'close', 'end']:
                break

            message = {'role': 'user', 'content': question}
            messages = [
                {'role': 'system', 'content': 'You are a very direct and straight-to-the-point assistant.'},
                *chat_history,
                message
            ]

            response = openai.ChatCompletion.create(model=model, messages=messages)

            text = response.choices[0].message.content.strip('\n')
            chat_history.append(message)
            chat_history.append({'role': 'assistant', 'content': text})
            if len(chat_history) > 4:
                chat_history.pop(0)

            print('\nAI: ', end='')
            for char in text:
                print(char, end='', flush=True)
                time.sleep(0.01)
            print('\n')
        except openai.error.APIError as e:
            print(f'OpenAI API returned an API Error: {e}')
            pass
        except openai.error.APIConnectionError as e:
            print(f'Failed to connect to OpenAI API: {e}')
            pass
        except openai.error.AuthenticationError as e:
            print(f'Invalid ApiKey: {e}')
            break
        except openai.error.RateLimitError as e:
            print(f'OpenAI API request exceeded rate limit: {e}')
            pass
        except openai.error.InvalidRequestError as e:
            print(f'Invalid request: {e}')
            break
        except KeyboardInterrupt:
            break
    print('\nAI: Goodbye')


if __name__ == '__main__':
    main()
