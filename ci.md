# CI

There's a `.github/workflows` folder in the root directory. The folder contains `ci.yml and cd.yml` files used for integration, testing and deployment.
These two files are chained as `cd.yml` depends on the successful completion of `ci.yml`

Here is a breakdown of key points in the `ci.yml` file.

## Workflow Trigger

The `on: workflow_call` indicates that this workflow is intended to be triggered by another workflow or a reusable workflow call. This allows it to be modular and reusable across different workflows.

## Jobs

The `test` job is the primary job that runs on `ubuntu-latest`. It uses a PostgreSQL database service to simulate the application’s environment for running tests.

## Services

A PostgreSQL container is created with the postgres:15-alpine image:

- Environment variables (`POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`) set up a database named kaya with kaya as the user and postgres as the password.

- Health checks ensure that the PostgreSQL service is ready before other steps proceed by running `pg_isready`.

## Steps

### Checkout Code

This uses the `actions/checkout@v4.1.1` action to pull the repository code into the runner environment.

### Set Up Python

The Python environment is set up using `actions/setup-python@v5` with version 3.10 and caching enabled for `pipenv`.

### Install System Dependencies

This installs essential system libraries and packages (`curl`, `libcurl4-openssl-dev`, `build-essential`, `libssl-dev`) needed for dependencies that may require system-level compilation.

### Install Pipenv

Pipenv, a dependency manager for Python projects, is installed by downloading and executing its installation script.

### Install Dependencies

Using `pipenv sync --dev`, both main and development dependencies listed in the Pipfile are installed, ensuring that the environment matches development requirements.

### Create .env File

A `.env` file is generated with key environment variables like `SECRET_KEY`, `DEBUG`, and database configurations (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASS`), which are necessary for Django to connect to the PostgreSQL database and run in a development configuration.

### Run pre-commit

`pre-commit` hooks are executed on all files using `pipenv run pre-commit run --all-files`. This step runs linters, formatters, or other checks defined in the pre-commit configuration to enforce code quality.

### Run Django Tests

- Django’s test suite is executed with `pipenv run python manage.py test -v 2`. This ensures that any issues or regressions in the code are detected.

- The necessary environment variables (`DJANGO_SETTINGS_MODULE`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASS`) are passed to enable Django to locate the database and use the correct settings.


## Summary

This workflow is structured to:

- Code quality checks are performed.
- The Django application is tested in an environment closely matching production.
- The workflow setup is modular, allowing easy reuse by other workflows.
