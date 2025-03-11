import glob
import os
import sys

import openai

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cli.core import ensure_api_key, read_stdin, valid_input, chatgpt_response, extract_prompt_and_file_args


def run():
    """
    gpt-refactor [api_key] [prompt] [file_pattern]
    """

    content = read_stdin()

    prompt, file_pattern, key_in_args = extract_prompt_and_file_args(content is None)

    if not valid_input(prompt) and not valid_input(content):
        print('No input provided by either stdin nor command argument. '
              'Usage example: gpt-refactor ./src/**/*.py "format this code"')
        sys.exit(1)

    if not valid_input(file_pattern):
        file_pattern = '*'

    openai.api_key = ensure_api_key(prompt=True, use_args_key=key_in_args)

    default_messages = [{'role': 'system', 'content': 'Return only the file content as a response!'}]

    if valid_input(content):
        default_messages.append({'role': 'user', 'content': str(content)})

    if valid_input(prompt):
        default_messages.append({'role': 'user', 'content': str(prompt)})

    for file_path in glob.glob(file_pattern, recursive=True):
        try:
            if os.path.isfile(file_path):
                messages = []
                messages.extend(default_messages)

                with open(file_path, 'r') as file:
                    file_content = file.read()
                    messages.append({'role': 'user', 'content': f'File content: {file_content}'})

                print(f"Refactoring {file_path}...")

                response = chatgpt_response(messages)
                if response is None:
                    sys.exit(2)

                if isinstance(response, str):
                    refactored_file = response
                else:
                    stream_content = ''
                    for token in response:
                        stream_content += token
                    refactored_file = stream_content

                if refactored_file.startswith('```'):
                    refactored_file = refactored_file.strip('` \n').split('\n', 1)[1].strip()

                with open(file_path, 'w') as f:
                    f.write(refactored_file)

                print(f"Refactored {file_path} successfully.")
        except Exception as e:
            print(f'Refactoring file {file_path} failed with error: {e}')


if __name__ == '__main__':
    run()
