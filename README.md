# ChatGPT - Command Line Interface

> CLI tool for interacting with ChatGPT using your favorite terminal

## Requirements

* Python >= 3.6
* OpenAI account and valid API key

## Installation

Tool can be installed using python3 `pip` command:

```sh
pip install chatgpt-cli-tool
```

Or you can install it directly form this project source:

```sh
python3 build.py

pip3 install dist/chatgpt-cli-tool-{version}.tar.gz
```

## Configuration

In order to use ChatGPT cli you will first need to register and create an API key on
the [official OpenAI website](https://platform.openai.com/account/api-keys).

Then you can configure the tool with your API key using any of the following options:

1. Set it through environment variable **OPENAI_API_KEY**
2. Create an **.env** file in the working directory with variable **OPENAI_API_KEY**
3. Pass it as the first argument when executing this script (e.g. `python main.py my_api_key`)

To see other configurable options for ChatGPT check out **.env.example** file.

## Running the CLI

If you installed the tool using pip, then simply start the cli using command:

```sh
chatgpt-cli your_api_key
```

If you are using source code, then first install the Python requirements:

```sh
pip install -r requirements.txt
```

Then, sse the following command to run this script:

```sh
python main.py [api_key] [org_id] [model]
```

All arguments are optional and if provided will override those defined using environment variables or **.env** file.

## License

ChatGPT-cli is [MIT licensed](LICENSE).