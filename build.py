import os
import shutil

shutil.rmtree('dist', ignore_errors=True)
os.system('python setup.py sdist bdist_wheel')
shutil.rmtree('chatgpt_cli_tool.egg-info', ignore_errors=True)

# Normalize package name to compy with PEP 625 standard
version_line = open('./cli/__init__.py', "rt").readline()
version = version_line.split('=')[-1].strip().replace('\'', '')
original_filename = f"./dist/chatgpt-cli-tool-{version}.tar.gz"
name_part, extension = os.path.splitext(original_filename)
parts = name_part.split('-')
distribution = '_'.join(parts[:-1])
new_filename = f"{distribution}-{version}{extension}"
os.rename(original_filename, new_filename)
