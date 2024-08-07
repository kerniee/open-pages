# Contributing to Open Pages

Welcome! Open Pages is always looking for contributors.

## Getting Started with Development

1. Fork the repository from GitHub UI

2. Clone the forked repository:

   ```bash
   git clone https://github.com/your-github-profile/open-pages.git
   # Alternatively, use ssh
   git clone git@github.com:your-github-profile/open-pages.git
   ```

3. Install poetry, a Python package manager. See the [official documentation](https://python-poetry.org/docs/).

4. Install dependencies:

   ```shell
   poetry install
   ```

5. Initialize pre-commit hooks:

   ```shell
   poetry run pre-commit install
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

Open Pull Request from your forked repository branch to the `master` branch in the main repository. Provide description
of your changes and make sure the pipeline is green.
