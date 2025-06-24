# Troubleshooting Log

This document records the challenges faced during the development and deployment of this project and the steps taken to resolve them.

---

### 1. DynamoDB Schema Mismatch and IAM Role Restrictions

#### Problem:

After setting up the application and configuring the AWS credentials, the `/secret` endpoint was returning an error:

```
{"secret_code":"Error connecting to DynamoDB: An error occurred (ValidationException) when calling the GetItem operation: The provided key element does not match the schema"}
```

This error indicated that the primary key used in the application's query (`code_name`, as specified in the `README.md`) did not match the actual primary key of the `devops-challenge` table in DynamoDB.

#### Troubleshooting Steps:

1.  **Initial Verification:** The code was checked against the `README.md` documentation, and they both consistently referred to the primary key as `code_name`. This suggested the documentation itself might be outdated or incorrect.

2.  **Attempted Schema Discovery:** To discover the correct primary key name, temporary debugging code was added to the `app/main.py` file to call the `dynamodb:DescribeTable` API action. This would programmatically fetch and print the table's schema.

3.  **IAM Permission Denial:** The attempt to describe the table failed with a new error:
    ```
    An error occurred (AccessDeniedException) when calling the DescribeTable operation... not authorized to perform: dynamodb:DescribeTable
    ```
    This revealed that the provided IAM user credentials were intentionally restricted and did not have the permissions to view the table's metadata. 
    As I don't have access to the AWS account and the user policy I couldn't troubleshoot it any further. 

#### Current Status:

The application is currently unable to retrieve data from DynamoDB, resulting in an error at the `/secret` endpoint. To find the correct primary key for the table and resolve the `ValidationException`, the IAM role's policy for the user should be checked. 

---

### 2. CI/CD Pipeline Blocked by Travis CI Free Plan Limitation

#### Problem:

The CI/CD pipeline, which was set up using Travis CI and defined in the `.travis.yml` file, could not be activated or run. Although the repository was correctly linked to Travis CI and the `.travis.yml` file was present in the root directory, no builds were triggered after multiple commits.

#### Troubleshooting Steps:

1.  **Repository Activation:** Verified that the GitHub repository was enabled in the Travis CI dashboard.
2.  **Configuration File:** Confirmed the `.travis.yml` file was correctly placed in the project's root directory.
3.  **Manual Trigger:** Pushed multiple empty commits to the repository to manually trigger a new build, but no builds appeared in the Travis CI UI.

#### Resolution:

The issue was identified as a limitation with the Travis CI account itself. The free trial, which is required to run builds on private or public repositories under the current `travis-ci.com` platform, was not available or had expired for the account. Without an active plan, Travis CI will not process any build jobs.

#### Current Status:

The CI/CD automation is currently blocked.