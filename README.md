# ChatGPT - Command Line Interface

> CLI tool for interacting with ChatGPT using your favorite terminal

## Requirements

* Python >= 3.6
* OpenAI account and valid API key

## Configuration

In order to use ChatGPT cli you will first need to register and create an API key on
the [official OpenAI website](https://platform.openai.com/account/api-keys).

Then you can configure the tool with your API key using any of the following options:

1. Set it through environment variable **OPENAI_API_KEY**
2. Create an **.env** file in the same directory as the script file with variable **OPENAI_API_KEY**
3. Pass it as the first argument when executing this script (e.g. `python main.py my_api_key`)

## Running the CLI

First install the Python requirements:

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