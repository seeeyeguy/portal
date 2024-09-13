# Pytest

## Description:

Pytest is a framework that allows us to write tests to verify and validate our Python code.


## Documentation:

For more details on the framework, including how-to guides on how to write tests,
please refer to the [official documentation](https://docs.pytest.org/en/7.1.x/index.html).

## How to run:
 
-   Here are various ways to run Pytest:

    1. Run all pytests: `docker compose exec api pytest`
    2. Run all pytests in a directory: `docker compose exec api pytest path/to/directory/from/inside/the/api/container`
    3. Run all pytests in a file: `docker compose exec api pytest path/to/file/from/inside/the/api/container/filename.py`. Note: Make sure to include the `.py` in the filename.
    4. Run all pytests on a specific test suite: `docker compose exec api pytest path/to/file/from/inside/the/api/container/filename.py::TestSuiteClass`. Note: Make sure to place the `::` characters between the filename and the class.
    5. Run a single test: `docker compose exec api pytest path/to/file/from/inside/the/api/container/filename.py::TestSuiteClass::test_method`. Note: Make sure to place the `::` characters at the adequate locations as shown.

-   Note: Be sure to include the prefix: `test_` in the file names of your test files to ensure Pytest can detect them.
