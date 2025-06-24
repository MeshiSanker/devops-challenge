from flask import Flask, jsonify
import os
import boto3

app = Flask(__name__)

# Fetch the secret from DynamoDB
def get_secret_from_dynamodb(code_name):
    """
    Fetches the secret code from the 'devops-challenge' DynamoDB table.
    """
    try:
        # These should be set as environment variables
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region = os.environ.get('AWS_REGION', 'eu-west-1')

        if not all([aws_access_key_id, aws_secret_access_key]):
            return "Error: AWS credentials not configured."

        dynamodb = boto3.resource(
            'dynamodb',
            region_name=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        table = dynamodb.Table('devops-challenge')
        response = table.get_item(
            Key={
                'code_name': code_name
            }
        )

        if 'Item' in response:
            return response['Item'].get('secret_code', 'Secret code not found in item.')
        else:
            return f"Error: Item with code_name '{code_name}' not found."
    except Exception as e:
        return f"Error connecting to DynamoDB: {str(e)}"

# Read the codeName from an environment variable, with 'thedoctor' as a default.
CODE_NAME = os.environ.get('CODE_NAME', 'thedoctor')

# A placeholder for the secret, to be fetched from DynamoDB
SECRET_CODE = get_secret_from_dynamodb(CODE_NAME)

@app.route('/health')
def health():
    """
    Health check endpoint.
    Returns the application status, GitHub project link, and Docker Hub link.
    """
    github_project_link = os.environ.get('GITHUB_PROJECT_LINK', "https://github.com/your-username/your-repo")
    docker_hub_link = os.environ.get('DOCKER_HUB_LINK', "https://hub.docker.com/r/your-username/your-repo")

    response = {
        "status": "healthy",
        "project": github_project_link,
        "container": docker_hub_link
    }
    return jsonify(response)

@app.route('/secret')
def secret():
    """
    Secret endpoint.
    Returns the secret code fetched from AWS DynamoDB.
    """
    response = {
        "secret_code": SECRET_CODE
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 