import os
import sys

from dotenv import load_dotenv

home_env_file = os.path.expanduser('~') + '/.chatgpt-cli/.env'
env_file = os.getcwd() + '/.env'


def find_api_key(default: str = None, prompt: bool = False) -> str:
    load_dotenv(home_env_file)
    load_dotenv(env_file)

    api_key = os.getenv('OPENAI_API_KEY', default)

    if len(sys.argv) > 1:
        api_key = str(sys.argv[1])

    if not is_valid(api_key):
        print(
            'API key not configured. You can configure API key in any of the following ways:\n'
            '1. Create an ~/.chatgpt-cli/.env file with variable OPENAI_API_KEY\n'
            '2. Create an .env file in the working directory with variable OPENAI_API_KEY\n'
            '3. Set it through environment variable OPENAI_API_KEY\n'
            '4. Pass it as the first argument when executing this script\n')

        if prompt is False:
            sys.exit(1)

        api_key = input('Or, you can enter the API key now: ')

        if not is_valid(api_key) or api_key.strip().lower() in ['no', 'exit', 'close', 'end']:
            sys.exit(2)
        else:
            answer = input(
                f'Do you want to save API key for future use (yes/no)? ')
            if answer == 'yes':
                home_dir = os.path.dirname(home_env_file)
                if not os.path.isdir(home_dir):
                    os.makedirs(home_dir, exist_ok=True)
                f = open(home_env_file, "w")
                f.write(f'OPENAI_API_KEY={api_key}')
                print(f'API key saved in {home_env_file}\n')

    return api_key if is_valid(api_key) else default


def is_valid(api_key: str) -> bool:
    return api_key is not None and api_key.strip() != ''
