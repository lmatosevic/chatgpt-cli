# ChatGPT - Command-Line Interface

![pypi](https://img.shields.io/pypi/v/chatgpt-cli-tool)
![license](https://img.shields.io/pypi/l/chatgpt-cli-tool)
![build](https://img.shields.io/badge/build-passing-brightgreen)

> CLI tool for interacting with ChatGPT using terminal

## Requirements

* Python >= 3.8.0
* OpenAI account and valid API key

## Installation

Tool can be installed using python3 `pip` command:

```sh
pip install chatgpt-cli-tool
```

Or you can install it directly form this project after building it:

```sh
python build.py

pip install dist/chatgpt-cli-tool-{version}.tar.gz
```

## Configuration

In order to use ChatGPT cli you will first need to register and create an API key on
the [official OpenAI website](https://platform.openai.com/account/api-keys).

Then you can configure the tool with your API key using any of the following options:

1. Create an **~/.chatgpt-cli/.env** file with variable **OPENAI_API_KEY**
2. Create an **.env** file in the working directory with variable **OPENAI_API_KEY**
3. Set it through environment variable **OPENAI_API_KEY**
4. Pass it as the first argument when executing this tool (e.g. `chatgpt-cli my_api_key [out_file]`)

All configurable environment variables for ChatGPT can be found in [.env.example](.env.example) file:

| Variable name       | Description                                                                                         | Default value                                              |
|---------------------|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| OPENAI_API_KEY      | OpenAI API key used to send request                                                                 | -                                                          |
| GPT_MODEL           | GPT model used for chat completion                                                                  | gpt-3.5-turbo                                              |
| GPT_TEMPERATURE     | GPT temperature value (between 0 and 2), lower values provide more focused and deterministic output | 1                                                          |
| GPT_STREAM_RESPONSE | Enable OpenAI client to use Server Sent Events for streaming tokens from the API                    | true                                                       |
| GPT_SYSTEM_DESC     | The description for the system on how to best tailor answers (disable with "None")                  | You are a very direct and straight-to-the-point assistant. |
| GPT_IMAGE_SIZE      | The generated image size (256x256, 512x512 or 1024x1024)                                            | 512x512                                                    |
| HISTORY_SIZE        | Number of last messages to keep in history as a context for the next question                       | 3                                                          |
| CHAT_TEXT_WIDTH     | Maximum number of characters to display per line in interactive chat mode (0 - as much as possible) | 0                                                          |
| CHAT_COLORED        | Enable this to use colors in interactive chat mode                                                  | true                                                       |
| CHAT_COLOR_YOU      | The color used for your inputs                                                                      | green                                                      |
| CHAT_COLOR_AI       | The colore of AI responses                                                                          | white                                                      |

_Supported ANSI colors are: black, red, green, yellow, blue, magenta, cyan, and white_

## Running the CLI

If you installed the tool using pip, then simply start the cli using any of the following commands:

### chatgpt-cli [api_key] [file_out]

This command starts interactive ChatGPT where you can chat with AI in form of a dialog.

```sh
# with api key and conversation output file path
chatgpt-cli my_api_key ./path/to/chat.txt

# with api key only
chatgpt-cli my_api_key

# with conversation output file
chatgpt-cli chat.txt

# without any arguments, api key is used from env variable and conversation is not saved to file
chatgpt-cli
```

If file does not exist it will be created together with all parent directories. Otherwise, if the file already exists
the user is prompted with 3 options on how to handle the existing file content:

1. Continue conversation
2. Keep previous content and start new conversation
3. Delete previous content and start new conversation

### gpt-ai [api_key] [query]

This comand sends single chat completion prompt for given query or content, and prints the result on stdout.

```sh
# with api key and query argument
gpt-ai my_api_key "What is ChatGPT?"

# with query argument
gpt-ai "What is ChatGPT?"

# with api key and piped input
cat file.txt | gpt-ai my_api_key

# with query from stdin
cat question.txt | gpt-ai

# with both query as argument and piped input
cat long-story.txt | gpt-ai "sumarize this text in 5 bullet points"

# with both query as argument and input directly from file
gpt-ai "explain this code" < main.py
```

### gpt-img [api_key] [prompt] [img_out]

This comand generates image for given prompt or content, and stores the image in provided output path or if not
specified, prints the binary result on stdout. Some terminals like PowerShell might malform the binary content when
outputing to file.

```sh
# with api key, prompt and output image path
gpt-img my_api_key "Robot walking a dog" ./my-images/image.png

# without api key
gpt-img "Robot walking a dog" ./my-images/image.png

# without output image path, the binary image data will be outputed to stdout
gpt-img "Robot walking a dog" > image.png

# with both piped input and argument prompts
cat description.txt | gpt-img "with cartoon graphics" ./image.png

# with only piped input and output image file
cat description.txt | gpt-img ./image.png

# with only piped input and output image directed to file
cat description.txt | gpt-img > ./image.png

# with only input directly from file, binary image data will be outputed to stdout
gpt-img < idea.txt
```

API key argument is optional for all commands, but if provided it will override API key defined using environment
variables.

## Examples

### Interactive mode

![interactive chat](https://github.com/lmatosevic/chatgpt-cli/blob/main/resources/chatgpt-cli-interactive.png?raw=true)

### Single query mode

![single command](https://github.com/lmatosevic/chatgpt-cli/blob/main/resources/chatgpt-cli-gpt-ai.png?raw=true)

## Recommendations

### ChatGPT-Slackbot

If you are a regular Slack user, check out my other project which provides seamless ChatGPT and Slack
integration: https://github.com/lmatosevic/chatgpt-slackbot

## License

ChatGPT-Cli is [MIT licensed](LICENSE).