import boto3
import json
import datetime

def get_db_credentials(secret_name, region_name="us-east-1"):
    """Retrieve database credentials from AWS Secrets Manager."""
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

def mask(value):
    """Mask a string for safe display."""
    if len(value) <= 4:
        return "****"
    return value[:2] + "*" * (len(value) - 4) + value[-2:]

if __name__ == "__main__":
    SECRET_NAME = "lab/m8-05/db-credentials"

    print(f"\n{'='*50}")
    print(f"  Secrets Manager Demo — {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}")

    print("\n[1] Retrieving secret from Secrets Manager...")
    creds = get_db_credentials(SECRET_NAME)

    print("\n[2] Connection info (password masked):")
    print(f"    Host:     {creds['host']}")
    print(f"    Port:     {creds['port']}")
    print(f"    Database: {creds['database']}")
    print(f"    Username: {creds['username']}")
    print(f"    Password: {mask(creds['password'])}")

    print("\n[3] Authentication method:")
    print("    No hardcoded credentials — using EC2 IAM Instance Profile")
    print("    Credentials: retrieved at runtime from Secrets Manager")
    print(f"\n    Secret ARN: {SECRET_NAME}")
    print(f"\n{'='*50}\n")
