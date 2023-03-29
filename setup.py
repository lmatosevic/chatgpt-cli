from setuptools import setup
from setuptools import find_packages

desc = "Command-line interface tool for interacting with ChatGPT using terminal"

verstrline = open('./cli/__init__.py', "rt").readline()
version = verstrline.split('=')[-1].strip().replace('\'', '')

setup(name="chatgpt-cli-tool",
      version=version,
      author="luka",
      author_email="lukamatosevic5@gmail.com",
      url='https://github.com/lmatosevic/chatgpt-cli',
      download_url=f'https://github.com/lmatosevic/chatgpt-cli/archive/refs/tags/{version}.tar.gz',
      packages=find_packages(),
      install_requires=["openai", "python-dotenv", "colorama"],
      python_requires='>=3.8.0',
      entry_points={
          'console_scripts': [
              'chatgpt-cli = cli:main.main',
              'gpt-ai = cli.command:ai.run',
              'gpt-img = cli.command:img.run'
          ]
      },
      keywords=['chatgpt', 'openai', 'dall-e', 'cli', 'chat'],
      description=desc)
