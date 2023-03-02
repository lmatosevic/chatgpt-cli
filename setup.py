from setuptools import setup
from setuptools import find_packages

desc = """\
ChatGPT-cli
==============

Command line interface tool for interacting with ChatGPT using your favorite terminal
"""

setup(name="chatgpt-cli-tool",
      version="1.0.3",
      author="luka",
      author_email="lukamatosevic5@gmail.com",
      url='https://github.com/lmatosevic/chatgpt-cli',
      download_url='https://github.com/lmatosevic/chatgpt-cli/archive/refs/tags/1.0.3.tar.gz',
      packages=find_packages(),
      install_requires=["openai", "python-dotenv"],
      python_requires='>=3.7.1',
      entry_points={
          'console_scripts': [
              'chatgpt-cli = cli:main.main'
          ]
      },
      keywords=['chatgpt', 'openapi', 'cli', 'chat'],
      description="ChatGPT command line interface",
      long_description=desc)
