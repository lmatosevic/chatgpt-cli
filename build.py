import os
import shutil


os.system('python setup.py sdist bdist_wheel')
shutil.rmtree('chatgpt_cli_tool.egg-info')