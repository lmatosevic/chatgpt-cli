import os
import sys

import openai

from cli.core import ensure_api_key, chatgpt_response, valid_input, default_system_desc


def run():
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
        print(f'Error: {e}')
        pass

    key_in_args = False
    if len(sys.argv) > 2:
        query = str(sys.argv[2])
        key_in_args = True
    elif len(sys.argv) > 1:
        query = str(sys.argv[1])
    else:
        query = None

    openai.api_key = ensure_api_key(prompt=True, use_args_key=key_in_args)

    if not valid_input(query) and not valid_input(content):
        print('No input provided by either stdin nor command argument. '
              'Usage example: cat long-story.txt | gpt-ai "sumarize this text in 5 bullet points"')
        sys.exit(1)

    messages = [
        {'role': 'system', 'content': default_system_desc}
    ]

    if valid_input(content):
        messages.append({'role': 'user', 'content': content})

    if valid_input(query):
        messages.append({'role': 'user', 'content': query})

    response = chatgpt_response(messages)
    if response is None:
        sys.exit(2)

    print(response)


if __name__ == '__main__':
    run()
