import os
import sys
from typing import List, TypedDict, Union, Optional

import openai
from dotenv import load_dotenv

from cli import __version__

home_env_file = os.path.expanduser('~') + '/.chatgpt-cli/.env'
env_file = os.getcwd() + '/.env'

default_model = 'gpt-3.5-turbo'
default_system_desc = 'You are a very direct and straight-to-the-point assistant.'

MessageType = TypedDict('MessageType', {'role': str, 'content': str})


def ensure_api_key(default: str = None, prompt: bool = False, use_args_key: bool = True) -> str:
    load_dotenv(home_env_file)
    load_dotenv(env_file)

    api_key = os.getenv('OPENAI_API_KEY', default)

    if len(sys.argv) > 1:
        value = sys.argv[1]
        if icase_contains(value, ['-v', '--version']):
            print(__version__)
            sys.exit(0)
        if use_args_key:
            api_key = str(sys.argv[1])

    if not valid_input(api_key):
        print(
            'API key not configured. You can configure API key in any of the following ways:\n'
            '1. Create an ~/.chatgpt-cli/.env file with variable OPENAI_API_KEY\n'
            '2. Create an .env file in the working directory with variable OPENAI_API_KEY\n'
            '3. Set it through environment variable OPENAI_API_KEY\n'
            '4. Pass it as the first argument when executing this script (e.g. chatgpt-cli your_api_key)\n')

        if prompt is False:
            sys.exit(1)

        api_key = input('Or, you can enter the API key now: ')

        if not valid_input(api_key) or icase_contains(api_key, ['no', 'exit', 'close', 'end']):
            sys.exit(1)
        else:
            save_key_answer = input(
                f'Do you want to save API key for future use (yes/no)? ')
            if icase_contains(save_key_answer, ['yes', 'y']):
                home_dir = os.path.dirname(home_env_file)
                if not os.path.isdir(home_dir):
                    os.makedirs(home_dir, exist_ok=True)
                f = open(home_env_file, "w")
                f.write(f'OPENAI_API_KEY={api_key}')
                print(f'API key saved in {home_env_file}\n')

    return api_key if valid_input(api_key) else default


def read_stdin() -> Union[str, None]:
    content = None
    try:
        f = open(0, 'r', encoding='utf-8')
        if f.seekable():
            f.seek(0, os.SEEK_CUR)
            old_file_position = f.tell()
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(old_file_position, os.SEEK_SET)
            if size > 0:
                content = f.read()
        else:
            if not sys.stdin.isatty():
                content = sys.stdin.read()
    except Exception as e:
        print(f'Error on stdin input: {e}')
        pass
    return content


def chatgpt_response(messages: List[MessageType]) -> Union[str, None]:
    if messages is None or len(messages) == 0:
        print('No messages provided')
        return None

    try:
        response = openai.ChatCompletion.create(model=default_model, messages=messages)
        return response.choices[0].message.content.strip('\n')
    except openai.error.APIError as e:
        print(f'OpenAI API returned an API Error: {e}')
        return None
    except openai.error.APIConnectionError as e:
        print(f'Failed to connect to OpenAI API: {e}')
        return None
    except openai.error.AuthenticationError as e:
        print(f'Invalid ApiKey: {e}')
        sys.exit(4)
    except openai.error.RateLimitError as e:
        print(f'OpenAI API request exceeded rate limit: {e}')
        return None
    except openai.error.InvalidRequestError as e:
        print(f'Invalid request: {e}')
        sys.exit(5)


def image_url_response(prompt: str) -> Union[str, None]:
    if prompt is None:
        print('Prompt not provided')
        return None
    try:
        response = openai.Image.create(prompt=prompt, n=1, size="512x512")
        return response.data[0].url
    except openai.error.APIError as e:
        print(f'OpenAI API returned an API Error: {e}')
        return None
    except openai.error.APIConnectionError as e:
        print(f'Failed to connect to OpenAI API: {e}')
        return None
    except openai.error.AuthenticationError as e:
        print(f'Invalid ApiKey: {e}')
        sys.exit(4)
    except openai.error.RateLimitError as e:
        print(f'OpenAI API request exceeded rate limit: {e}')
        return None
    except openai.error.InvalidRequestError as e:
        print(f'Invalid request: {e}')
        sys.exit(5)


def valid_input(value: Optional[str]) -> bool:
    return value is not None and value.strip() != ''


def icase_contains(value: Optional[str], items: List[str]) -> bool:
    return valid_input(value) and value.strip().lower() in items


def valid_api_key(value: str) -> bool:
    return value.strip().startswith('sk-') and ' ' not in value.strip() and len(value.strip()) >= 48
