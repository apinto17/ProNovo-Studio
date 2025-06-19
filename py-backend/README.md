# Get Started

1. First install poetry

- `pip install pipx`
- `pipx install poetry`

2. Install dependencies from the poetry lock file

- `poetry install`

3. Then, go into py-backend/ and run

- `poetry run fastapi dev src/main.py`

# To make vscode play nice

Set your interpretor to use the poetry environment

1. First run `poetry env info --path`

- That will get you a path where your poetry environment is

2. Then click on the command pallete via the gear icon in the bottom left of the screen

3. Type "Python: Select Interpreter" and paste your env path _plus_ /bin/python at the end, so it should look like this:

/Users/alexpinto/Library/Caches/pypoetry/virtualenvs/py-backend-RVjEZLhN-py3.12/bin/python
