import sys

import openai

from cli.core import ensure_api_key, read_stdin, valid_api_key, valid_input, chatgpt_response


def run():
    """
    gpt-ai [api_key] [query]
    """

    content = read_stdin()

    key_in_args = False
    if len(sys.argv) > 2:
        query = str(sys.argv[2])
        key_in_args = True
    elif len(sys.argv) > 1:
        query = str(sys.argv[1])
        if valid_api_key(query):
            key_in_args = True
            query = None
    else:
        query = None

    openai.api_key = ensure_api_key(prompt=True, use_args_key=key_in_args)

    if not valid_input(query) and not valid_input(content):
        print('No input provided by either stdin nor command argument. '
              'Usage example: cat long-story.txt | gpt-ai "sumarize this text in 5 bullet points"')
        sys.exit(1)

    messages = []

    if valid_input(content):
        messages.append({'role': 'user', 'content': str(content)})

    if valid_input(query):
        messages.append({'role': 'user', 'content': str(query)})

    response = chatgpt_response(messages)
    if response is None:
        sys.exit(2)

    print(response)


if __name__ == '__main__':
    run()
