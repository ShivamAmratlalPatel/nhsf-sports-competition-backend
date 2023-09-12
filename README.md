# FastAPI Backend Application

This is a Python backend application built using the FastAPI framework. It provides a RESTful API for interacting with the application's functionality.


## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- [Python 3.11](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)

## Setup

1. Install project dependencies using Poetry:

    ```bash
    poetry install
    ```

## Running the Application

To start the FastAPI application, follow these steps:

1. Start the application using Docker Compose:

    ```bash
    docker-compose up
    ```

2. Migrate the database:

    ```bash
    docker exec -it nhsf-backend sh ./scripts/migrate.sh
    ```
   
3. Navigate to the application's Swagger documentation at [http://localhost:8001/docs](http://localhost:8001/docs).

## Generating a New Migration

If you have made changes to the database models, you will need to generate a new migration. To do this:

1. Make sure the application is running.
2. In /scripts/generate_migration.sh, change the `$x` to a description of the migration e.g. `add new column to user model`.
3. Run the following command:

```bash
docker exec -it nhsf-backend sh ./scripts/generate_migration.sh
```

## Testing

To run all tests, run:

```bash
docker exec -it nhsf-backend pytest
```

To run a specific test, run:

```bash
docker exec -it nhsf-backend pytest ./testing/test_file.py::test_name
```

## Pre-commit Hooks

This project includes pre-commit hooks, which are automated checks that run before each commit to ensure code quality and maintain consistency. The hooks are managed using [pre-commit](https://pre-commit.com/).

To set up the pre-commit hooks, run the following command after installing the project dependencies:
    
 ```bash
 poetry run pre-commit install
 ```

You can check it worked by running manually with:

 ```bash
 poetry run pre-commit run --all-files
 ```

## Linting

This project uses [ruff](https://beta.ruff.rs/docs/) for linting. To run the linter, run the following command:

```bash
poetry run ruff check .
```

Optionally you can run the linter with the `--fix` flag to automatically fix any linting errors:

```bash
poetry run ruff check . --fix
```

## Formatting

This project uses [black](https://black.readthedocs.io/en/stable/) for formatting. To run the formatter, run the following command:

```bash
poetry run black .
```

This project also uses [isort](https://pycqa.github.io/isort/) for sorting imports. To run the import sorter, run the following command:

```bash
poetry run isort .
```

Both of these run with pre-commit hooks, so you shouldn't need to run them manually.

## PyCharm Setup

### Python Interpreter

For this project, you can either use a local Python interpreter or a Docker interpreter.
The Docker interpreter is recommended as it will be more consistent across different machines.
The Docker interpreter will be needed to run tests which require a database.

#### Docker Interpreter

1. Open the project in PyCharm.
2. Go to `File > Settings > Project: nhsf-backend > Python Interpreter`.
3. Click the gear icon and select `Add`.
4. Select `On Docker Compose`.
5. Select the `docker-compose.yml` file in the root of the project.
6. Select the `backend` service.
7. Click `Next`.
8. Click `Next` again.
9. Select `System Interpreter`.
10. The interpreter path should be `/usr/local/bin/python`, not `/usr/local/bin/python3`.
11. Click `Create`.

#### Local Interpreter
1. Open the project in PyCharm.
2. Go to `File > Settings > Project: nhsf-backend > Python Interpreter`.
3. Click the gear icon and select `Add`.
4. Select `Add Local Interpreter`.
5. Select `Poetry Environment` from the left-hand menu.
6. Make sure the base interpreter is set to your local Python 3.11 installation.
7. Click `OK`.

### Running tests in PyCharm

1. Go to `Run > Edit Configurations`.
2. Click the `+` icon and select `Python tests > pytest`.
3. Set the name to `pytest`.
4. Set the target to `Script path` and enter the testing directory.
5. Make sure the interpreter is set to the Docker interpreter.
6. Set the working directory to the root of the project.

#### Running an individual test

1. Click the play button next to the test you want to run.
2. Initially this will fail as the working directory is not set correctly.
3. Click edit configuration and set the working directory to the root of the project.
4. Rename the test path to include the path from the root of the project to the test file.
5. Click `OK`.
6. Click the play button again.

### Commit settings

1. Go to `File > Settings > Version Control > Commit`.
2. There you can have PyCharm automatically run the tests on each commit by selecting `Run tests` and selecting the `pytest` configuration.
3. Also selecting `Run git hooks` will run the pre-commit hooks on each commit.


### File Watchers

1. Go to `File > Settings > Tools > File Watchers`.
2. Click the `+` icon and select `Custom`.
3. Set the name to `black`.
4. Set the file type to `Python`.
5. Set the scope to `Project Files`.
6. Set the program to the Docker interpreter.
7. Set the arguments to `black --quiet $FilePathRelativeToProjectRoot$`.
8. Set the working directory to `$ProjectFileDir$`.
9. Click `OK`.

### Actions on Save

1. Go to `File > Settings > Tools > Actions on Save`.
2. Disable `Reformat code`.
3. Enable `Run File Watchers`.

### Backend Import Errors

If you are getting import errors in the backend, try setting nhsf-backend as a Sources Root.



   

