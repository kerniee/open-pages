# Contributing to Open Pages

Welcome! Open Pages is always looking for contributors.

## Getting Started with Development

1. Clone the repository:

   ```bash
   git clone https://github.com/kerniee/open-pages.git
   ```

2. Install poetry, a Python package manager. See the [official documentation](https://python-poetry.org/docs/).

3. Install dependencies:

   ```shell
   poetry install
   ```

4. Install tool called pre-commit. See the [official documentaion](https://pre-commit.com/).

5. Initialize pre-commit hooks:

   ```shell
   pre-commit install
   ```

6. Run the development server:

    ```shell
    poetry run fastapi dev open_pages/main.py
    ```

   You can also run tests:

    ```shell
    poetry run pytest
    ```

## Commits

Create new branch, commit and push your changes to this new branch. Please, follow conventional commit guidelines for
commit naming.

## Submitting changes

Open Pull Request from your branch to the `master` branch. Provide description of your changes and make sure the
pipeline is green.
