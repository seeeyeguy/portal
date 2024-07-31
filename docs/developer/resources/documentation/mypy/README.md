# MyPy

## Description:
MyPy is static type checker tool for Python files. By using this tool, along with static typing in our Python code, we make it easier to understand and less prone to introducing bugs.

## Documentation:
For more details on MyPy, please refer to the [official documentation](
https://mypy.readthedocs.io/en/stable/).

## How to run:
 
1. Set `PYTHONPATH` on your bash terminal to `./api/src` by running the command: `export PYTHONPATH=./api/src`.
2. Verify the value of `PYTHONPATH` by running: `echo $PYTHONPATH`.
3. Run the mypy command: `mypy api/src --config=api/mypy.ini`.
