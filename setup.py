from setuptools import setup
from setuptools import find_packages

desc = "Command-line interface tool for interacting with ChatGPT using terminal"

version_line = open('./cli/__init__.py', "rt").readline()
version = version_line.split('=')[-1].strip().replace('\'', '')

with open('./requirements.txt', 'r') as file:
    requirements = [line.strip() for line in file]

setup(name="chatgpt-cli-tool",
      version=version,
      author="luka",
      author_email="lukamatosevic5@gmail.com",
      license="MIT",
      url='https://github.com/lmatosevic/chatgpt-cli',
      download_url=f'https://github.com/lmatosevic/chatgpt-cli/archive/refs/tags/{version}.tar.gz',
      packages=find_packages(),
      install_requires=requirements,
      python_requires='>=3.8.0',
      entry_points={
          'console_scripts': [
              'chatgpt-cli = cli:main.main',
              'gpt-ai = cli.command:ai.run',
              'gpt-img = cli.command:img.run',
              'gpt-refactor = cli.command:refactor.run'
          ]
      },
      keywords=['chatgpt', 'openai', 'dall-e', 'cli', 'chat'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11'
      ],
      description=desc)
