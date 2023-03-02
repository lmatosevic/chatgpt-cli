import os
import sys
import time

import openai
from dotenv import load_dotenv

default_api_key = None
default_org_id = None
default_model = 'gpt-3.5-turbo'


def main():
    load_dotenv()

    api_key = None
    org_id = None

    if len(sys.argv) > 1:
        api_key = str(sys.argv[1])

    if len(sys.argv) > 2:
        org_id = str(sys.argv[2])

    if len(sys.argv) > 3:
        model = str(sys.argv[3])
    else:
        model = os.getenv('OPENAI_MODEL', default_model)

    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY', default_api_key)
        org_id = os.getenv('OPENAI_ORG_ID', default_org_id)

    if org_id is None:
        org_id = os.getenv('OPENAI_ORG_ID', None)

    if api_key is None:
        print(
            'API key not configured. You can configure API key in any of the following ways:\n'
            '1. Set it through environment variable OPENAI_API_KEY\n'
            '2. Create an .env file in the same directory as the script with variable OPENAI_API_KEY\n'
            '3. Pass it as the first argument when executing this script')
        sys.exit(1)

    openai.api_key = api_key
    openai.organization = org_id

    print(f'Welcome to the ChatGPT command line interface\n')
    print(f'Please enter your question (type "exit" to stop chatting)\n')

    end = False
    chat_history = []
    while end is False:
        try:
            question = input('You: ')

            if question is None or question.strip() == '':
                continue

            if question in ['exit', 'quit', 'close', 'end']:
                break

            message = {'role': 'user', 'content': question}
            messages = [
                {'role': 'system', 'content': 'You are very direct and straight to the point assistant.'},
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
