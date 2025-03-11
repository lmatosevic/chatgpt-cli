import os
import shutil

package_name = 'chatgpt_cli_tool'

# Clear and build package files
shutil.rmtree('dist', ignore_errors=True)
os.system('python setup.py sdist bdist_wheel')
shutil.rmtree(f'{package_name}.egg-info', ignore_errors=True)

# Normalize package name to compy with PEP 625 standard
version_line = open('./cli/__init__.py', "rt").readline()
version = version_line.split('=')[-1].strip().replace('\'', '')
os.rename(f"./dist/{package_name.replace('_', '-')}-{version}.tar.gz", f"./dist/{package_name}-{version}.tar.gz")
