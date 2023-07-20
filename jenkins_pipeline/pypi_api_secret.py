import boto3
from botocore.exceptions import ClientError


def get_pypi_api_token():

    secret_name = "pypi_api_token"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as error:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise error

    # Decrypts secret using the associated KMS key.
    return get_secret_value_response['SecretString']