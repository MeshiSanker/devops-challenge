# Instructions

This document provides instructions on how to run and test this project.

## Prerequisites

- Docker
- Docker Compose

## Setup

1.  Clone the repository.
2.  Create a `.env` file from the template:
    ```bash
    cp env.template .env
    ```
3.  Edit `.env` and fill in the required values:
    - `GITHUB_PROJECT_LINK`: Your project's GitHub repository URL.
    - `DOCKER_HUB_LINK`: The URL for your container image on Docker Hub.
    - `CODE_NAME`: The code name to look up in DynamoDB.
    - `AWS_ACCESS_KEY_ID`: Your AWS access key.
    - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key.
    - `AWS_REGION`: The AWS region for the DynamoDB table.

    **Note:** The `.env` file contains sensitive information and is ignored by Git. Do not commit it.

## Running the Application

To start the application, run:

```bash
docker-compose up --build -d
```

The application will be available at `http://127.0.0.1:5000`.

You can view the application logs with:
```bash
docker-compose logs -f web
```

To stop the application:
```bash
docker-compose down
```

## Running Tests

To run the test suite, use the following command:

```bash
docker-compose run --rm test
```

This command uses the `test` service defined in `docker-compose.yml` to run the tests inside a container. 