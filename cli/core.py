import os
import sys
from typing import List, TypedDict, Union, Optional, Tuple, Iterable

import openai
from dotenv import load_dotenv

from cli import __version__

home_env_file = os.path.expanduser('~') + '/.chatgpt-cli/.env'
env_file = os.getcwd() + '/.env'

load_dotenv(home_env_file)
load_dotenv(env_file)

default_model = 'gpt-3.5-turbo'
default_temperature = '1'
default_stream_response = 'true'
default_system_desc = 'You are a very direct and straight-to-the-point assistant.'
default_image_model = 'dall-e-2'
default_image_size = '1024x1024'

MessageType = TypedDict('MessageType', {'role': str, 'content': str})


def ensure_api_key(default: str = None, prompt: bool = False, use_args_key: bool = True) -> str:
    """
    Ensures that the OpenAI API key is configured.

    This function checks the environment for the API key and attempts to retrieve it.
    If not available, it prompts the user to provide the key, and optionally saves it
    for future use.

    Args:
        default (str, optional): A default API key to return if none is found.
        prompt (bool, optional): Whether to prompt for the key if not found. Defaults to False.
        use_args_key (bool, optional): Whether to use the API key provided as a command line argument. Defaults to True.

    Returns:
        str: The OpenAI API key.
    """
    api_key = get_env('OPENAI_API_KEY', default)

    if len(sys.argv) > 1:
        value = sys.argv[1]
        if icase_contains(value, ['-v', '--version']):
            print(__version__)
            sys.exit(0)
        if use_args_key:
            api_key = str(sys.argv[1])

    if not valid_input(api_key):
        print(
            'OpenAI API key is not configured. If you don\'t have OpenAI API key yet, you can create it here: '
            'https://platform.openai.com/account/api-keys\n\n'
            'The API key can be configured in any of the following ways:\n'
            '1. Create an ~/.chatgpt-cli/.env file with variable OPENAI_API_KEY\n'
            '2. Create an .env file in the working directory with variable OPENAI_API_KEY\n'
            '3. Set it through environment variable OPENAI_API_KEY\n'
            '4. Pass it as the first argument when executing this script (e.g. chatgpt-cli your_api_key [out_file])\n')

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


def check_args_for_key() -> Tuple[bool, str]:
    """
    Checks the command line arguments for an API key.

    This function looks through the command line arguments to determine if an API key
    is provided. It returns a boolean indicating if a key was found and the key itself.

    Returns:
        Tuple[bool, str]: A tuple where the first element is a boolean indicating 
                          if a key is found, and the second element is the key or None.
    """
    key_in_args = False
    if len(sys.argv) > 2:
        value = str(sys.argv[2])
        key_in_args = True
    elif len(sys.argv) > 1:
        value = str(sys.argv[1])
        if valid_api_key(value):
            key_in_args = True
            value = None
    else:
        value = None
    return key_in_args, value


def read_stdin() -> Union[str, None]:
    """
    Reads input from standard input (stdin).

    This function attempts to read content from standard input and returns it as a string.
    If no content is available, it returns None.

    Returns:
        Union[str, None]: The input content read from stdin or None if no content is available.
    """
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


def extract_prompt_and_file_args(no_content: bool = False) -> Tuple[str, str, bool]:
    """
    Extracts the prompt and file arguments from the command line.

    This function analyzes the command line arguments to separate the prompt from file path and 
    checks if an API key is provided in the arguments.

    Args:
        no_content (bool, optional): Indicates if content should be treated as the prompt. Defaults to False.

    Returns:
        Tuple[str, str, bool]: A tuple containing the prompt, file path, and a boolean indicating 
                               if a key was found in the arguments.
    """
    key_in_args = False
    if len(sys.argv) > 3:
        file_path = str(sys.argv[3])
        prompt = str(sys.argv[2])
        key_in_args = True
    elif len(sys.argv) > 2:
        file_path = str(sys.argv[2])
        prompt = str(sys.argv[1])
        if valid_api_key(prompt):
            key_in_args = True
            prompt = None
            if no_content:
                prompt = file_path
                file_path = None
    elif len(sys.argv) > 1:
        file_path = str(sys.argv[1])
        prompt = None
        if valid_api_key(file_path):
            key_in_args = True
            file_path = None
            prompt = None
        elif no_content:
            prompt = file_path
            file_path = None
    else:
        file_path = None
        prompt = None
    return prompt, file_path, key_in_args


def chatgpt_response(messages: List[MessageType]) -> Union[str, Iterable[str], None]:
    """
    Sends a chat message to the GPT model and retrieves the response.

    This function takes a list of messages, sends them to the OpenAI ChatCompletion API,
    and returns the response. It supports both streaming and non-streaming responses.

    Args:
        messages (List[MessageType]): A list of message dictionaries containing role and content.

    Returns:
        Union[str, Iterable[str], None]: The response from the API as a string if not streaming, 
                                           otherwise yields chunks of response in streaming mode, 
                                           or None in case of errors.
    """
    if messages is None or len(messages) == 0:
        print('No messages provided')
        return None

    model = get_env('GPT_MODEL', default_model)
    temperature = float(get_env('GPT_TEMPERATURE', default_temperature))
    stream = icase_contains(get_env('GPT_STREAM_RESPONSE', default_stream_response), ['true', 'yes', 'on'])
    system_desc = get_env('GPT_SYSTEM_DESC', default_system_desc)

    if system_desc.lower() != 'none':
        messages.insert(0, {'role': 'system', 'content': system_desc})

    try:
        response = openai.ChatCompletion.create(model=model, temperature=temperature, messages=messages, stream=stream)
        if not stream:
            return response.choices[0].message.content.strip('\n')

        def stream_response() -> Iterable[str]:
            for line in response:
                chunk = line['choices'][0].get('delta', {}).get('content', '')
                if chunk:
                    yield chunk

        return stream_response()
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
    """
    Generates an image URL based on the given prompt.

    This function sends the prompt to OpenAI's image generation API and retrieves the URL of the generated image.

    Args:
        prompt (str): The prompt for which to generate an image.

    Returns:
        Union[str, None]: The URL of the generated image or None in case of errors.
    """
    if prompt is None:
        print('Prompt not provided')
        return None

    image_model = get_env('GPT_IMAGE_MODEL', default_image_model)
    image_size = get_env('GPT_IMAGE_SIZE', default_image_size)

    try:
        response = openai.Image.create(model=image_model, prompt=prompt, n=1, size=image_size)
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
    """
    Validates a string input.

    This function checks if the provided value is not None and not just whitespace.

    Args:
        value (Optional[str]): The string input to validate.

    Returns:
        bool: True if the input is valid, otherwise False.
    """
    return value is not None and value.strip() != ''


def icase_contains(value: Optional[str], items: List[str]) -> bool:
    """
    Checks if a given value, case-insensitively, is contained in a list of items.

    Args:
        value (Optional[str]): The value to check.
        items (List[str]): The list of items to search within.

    Returns:
        bool: True if the value is found in items, otherwise False.
    """
    return valid_input(value) and value.strip().lower() in items


def valid_api_key(value: str) -> bool:
    """
    Validates an OpenAI API key.

    This function checks if the API key starts with 'sk-', does not contain whitespace, 
    and has the appropriate length.

    Args:
        value (str): The API key to validate.

    Returns:
        bool: True if the API key is valid, otherwise False.
    """
    return value.strip().startswith('sk-') and ' ' not in value.strip() and len(value.strip()) >= 48


def get_env(key: str, default: Optional[str]) -> str:
    """
    Retrieves an environment variable.

    This function gets the value for the specified key from the environment and returns 
    the default if not set.

    Args:
        key (str): The environment variable key to retrieve.
        default (Optional[str]): The default value if the key is not found.

    Returns:
        str: The value of the environment variable or the default.
    """
    value = os.getenv(key, default)
    if not valid_input(value):
        value = default
    return value
