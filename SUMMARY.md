# Project Plan

This document outlines the plan for the DevOps Challenge.

### Revised Project Plan

#### Phase 1: Project Setup & Application Development
- Create the Flask web application with `/secret` and `/health` endpoints.
- Write the logic to fetch the secret from AWS DynamoDB.
- Externalize configuration to an `.env` file.

#### Phase 2: Containerization with Docker
- Write a `Dockerfile` for the application.
- Create a `docker-compose.yml` file.

#### Phase 3: CI/CD Automation with Travis CI
- Create a `.travis.yml` file to test, build, and push your Docker image to Docker Hub.

#### Phase 4: Documentation
- Create `SUMMARY.md`, `TROUBLE.md`, and `INSTRUCTIONS.md`.

#### Phase 5: Final Verification
- Use `verification.sh` to do a final end-to-end check of the running system.

---

### Development and Troubleshooting Log

#### Phase 2: Containerization with Docker

- **`Dockerfile` Creation:** A `Dockerfile` was created in the root directory. It uses the `python:3.9-slim` base image, sets up the working directory, installs dependencies from `requirements.txt`, and copies the application code. It exposes port 5000 and runs the Flask application.

- **`docker-compose.yml` Creation:** A `docker-compose.yml` file was created to simplify local development. It defines a single `web` service that builds the image using the `Dockerfile`, maps port 5000, and loads environment variables from the `.env` file.

- **DynamoDB and IAM Troubleshooting:** A significant challenge was encountered when connecting to DynamoDB. The application initially failed with a `ValidationException`, indicating that the primary key (`code_name`) specified in the `README.md` was incorrect. An attempt to programmatically discover the key schema failed due to an `AccessDeniedException`, revealing that the provided IAM user permissions were restricted. This issue is documented in `TROUBLE.md` and currently blocks the retrieval of the secret.

#### Phase 3: CI/CD Automation with Travis CI

- **Manual Docker Hub Push:** Before automating the process with Travis CI, the Docker image was pushed manually to Docker Hub. This involved logging in, tagging the locally built image (`devops-challenge-web`) with the correct repository name (`meshisanker/devops-challenge`), and pushing it. The repository had to be created on Docker Hub first to avoid a "repository does not exist" error.

- **`.travis.yml` and Unit Tests:** A `.travis.yml` file was created to define the CI/CD pipeline. The configuration specifies a Python environment, installs dependencies, and runs unit tests. A test suite (`test/test_app.py`) was developed to validate the application's endpoints (`/health` and `/secret`) and to mock the DynamoDB interactions, ensuring the tests could run independently of AWS services.

- **Travis CI Activation Issues:** After setting up the configuration and tests, it was discovered that the builds were not running. The troubleshooting process confirmed that the issue was not with the repository setup but with the Travis CI account itself, which lacked an active free plan. This problem has been documented in `TROUBLE.md`.

#### Phase 4: Documentation
- Create `SUMMARY.md`, `TROUBLE.md`, and `INSTRUCTIONS.md`.

#### Phase 5: Final Verification
- Use `verification.sh` to do a final end-to-end check of the running system. 