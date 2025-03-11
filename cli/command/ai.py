import os
import sys

import openai

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cli.core import ensure_api_key, read_stdin, check_args_for_key, valid_input, chatgpt_response


def run():
    """
    gpt-ai [api_key] [prompt]
    """

    content = read_stdin()

    key_in_args, prompt = check_args_for_key()

    if not valid_input(prompt) and not valid_input(content):
        print('No input provided by either stdin nor command argument. '
              'Usage example: cat long-story.txt | gpt-ai "sumarize this text in 5 bullet points"')
        sys.exit(1)

    openai.api_key = ensure_api_key(prompt=True, use_args_key=key_in_args)

    messages = []

    if valid_input(content):
        messages.append({'role': 'user', 'content': str(content)})

    if valid_input(prompt):
        messages.append({'role': 'user', 'content': str(prompt)})

    response = chatgpt_response(messages)
    if response is None:
        sys.exit(2)

    if isinstance(response, str):
        print(response)
    else:
        stream_content = ''
        for token in response:
            stream_content += token
        print(stream_content)


if __name__ == '__main__':
    run()
