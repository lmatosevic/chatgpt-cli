import os
import shutil

shutil.rmtree('dist', ignore_errors=True)
os.system('python setup.py sdist bdist_wheel')
shutil.rmtree('chatgpt_cli_tool.egg-info', ignore_errors=True)
