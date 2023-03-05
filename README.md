# ChatGPT - Command-Line Interface

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
4. Pass it as the first argument when executing this tool (e.g. `chatgpt-cli my_api_key`)

To see other configurable options for ChatGPT check out **.env.example** file.

## Running the CLI

If you installed the tool using pip, then simply start the cli using any of the following commands:

### chatgpt-cli [api_key]

```sh
# with api key
chatgpt-cli my_api_key

# without api key
chatgpt-cli
```

### gpt-ai [api_key] [query]

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

# with only input directly from file, binary image data will be outputed to stdout
gpt-img < idea.txt
```

API key argument is optional, but if provided it will override API key defined using environment variables.

## License

ChatGPT-cli is [MIT licensed](LICENSE).