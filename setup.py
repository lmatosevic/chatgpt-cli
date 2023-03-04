from setuptools import setup
from setuptools import find_packages

desc = "Command line interface tool for interacting with ChatGPT using terminal"

version = "1.1.0"

setup(name="chatgpt-cli-tool",
      version=version,
      author="luka",
      author_email="lukamatosevic5@gmail.com",
      url='https://github.com/lmatosevic/chatgpt-cli',
      download_url=f'https://github.com/lmatosevic/chatgpt-cli/archive/refs/tags/{version}.tar.gz',
      packages=find_packages(),
      install_requires=["openai", "python-dotenv"],
      python_requires='>=3.7.1',
      entry_points={
          'console_scripts': [
              'chatgpt-cli = cli:main.main'
          ]
      },
      keywords=['chatgpt', 'openapi', 'cli', 'chat'],
      description=desc)
