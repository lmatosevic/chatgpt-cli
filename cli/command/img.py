import os
import sys
from urllib.request import urlopen

import openai

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cli.core import ensure_api_key, read_stdin, valid_input, image_url_response, extract_prompt_and_file_args


def run():
    """
    Execute the main functionality of the gpt-img application.

    This function reads input from standard input or command line arguments,
    validates the input, retrieves an image based on the provided prompt, 
    and writes the image to standard output or a specified file.

    Command-line usage:
        gpt-img [api_key] [prompt] [img_out]

    If no prompt is provided via the command line or standard input, the
    function will print an error message and exit with status code 1.
    If there is an error retrieving the image, it will exit with status code 2.

    Returns:
        None
    """

    content = read_stdin()

    prompt, img_out, key_in_args = extract_prompt_and_file_args(content is None)

    if not valid_input(prompt) and not valid_input(content):
        print('No input provided by either stdin nor command argument. '
              'Usage example: cat description.txt | gpt-img "with cartoon graphics" out.png')
        sys.exit(1)

    openai.api_key = ensure_api_key(prompt=True, use_args_key=key_in_args)

    combined_prompt = ''
    if valid_input(content):
        combined_prompt = combined_prompt + content
    if valid_input(prompt):
        if len(combined_prompt) > 0:
            combined_prompt = combined_prompt + '. '
        combined_prompt = combined_prompt + prompt

    response = image_url_response(combined_prompt)
    if response is None:
        sys.exit(2)

    img = urlopen(response).read()

    if img_out is None:
        stdout = os.fdopen(sys.stdout.fileno(), "wb", closefd=False)
        stdout.write(img)
        stdout.flush()
    else:
        image_file = open(img_out, 'wb')
        image_file.write(img)
        image_file.close()


if __name__ == '__main__':
    run()
