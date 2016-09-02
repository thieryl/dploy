"""
Project Tasks that can be invoked using using the program "invoke" or "inv"
"""

import os
import glob
from invoke import task

# disable the check for unused-arguments to ignore unused ctx parameter in tasks
# pylint: disable=unused-argument

@task
def setup(ctx):
    """
    Install python requirements
    """
    ctx.run('pip install -r requirements.txt')

@task
def clean(ctx):
    """
    Clean repository using git
    """
    ctx.run('git clean --interactive', pty=True)

@task
def lint(ctx):
    """
    Run pylint on this module
    """
    files = [
        'dploy',
        'setup.py',
        'tasks.py',
    ]
    files.extend(glob.glob(os.path.join('tests', '*.py')))
    files_string = ' '.join(files)
    cmd = 'python3 -m pylint --output-format=parseable {files}'
    ctx.run(cmd.format(files=files_string))

@task
def test(ctx):
    """
    Test Task
    """
    cmd = 'py.test'
    ctx.run(cmd)

@task(test, lint, default=True)
def default(ctx):
    """
    Default Tasks
    """
    pass

@task(clean)
def build(ctx):
    """
    Task to build an executable using pyinstaller
    """
    cmd = 'pyinstaller -n dploy --onefile ' + os.path.join('dploy', '__main__.py')
    ctx.run(cmd)