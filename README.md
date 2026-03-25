# Lab M8.05 - Store First Secret in Secure System (Secrets Manager)

**Repository:** https://github.com/MaryaAhmadi/ce-lab-store-first-secret.git

**Activity Type:** Individual  
**Estimated Time:** 45 minutes


## Overview

In this lab, I implemented a secure pattern for handling application credentials using AWS Secrets Manager and IAM Roles. Instead of hardcoding database credentials inside the application, the EC2 instance retrieves them dynamically at runtime using an attached IAM role.
This approach eliminates the need for storing access keys or sensitive data in code, making the system more secure and production-ready.

## Architecture Summary
The solution consists of the following components:
* AWS Secrets Manager
    * Stores database credentials securely (username, password, host, port, database)
* IAM Policy (Least Privilege)
    * Grants only:
        * secretsmanager:GetSecretValue
        * secretsmanager:DescribeSecret
    * Scoped to a single secret ARN
* IAM Role + Instance Profile
    * Attached to EC2
    * Enables secure access without AWS access keys
* EC2 Instance (Amazon Linux 2)
    * Runs a Python application
    * Retrieves secrets dynamically via boto3
* Python Application
    * Fetches secret at runtime
    * Displays masked credentials
    * Demonstrates secure access pattern

## Secret Details

* Secret Name: lab/m8-05/db-credentials
* Region: us-east-1
Stored JSON Structure:
{
  "username": "app_user",
  "password": "******",
  "host": "mydb.cluster-abc.us-east-1.rds.amazonaws.com",
  "port": 5432,
  "database": "appdb"
}



## Application Code

The application retrieves the secret dynamically using boto3:
import boto3
import json

def get_db_credentials(secret_name):
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])
Key point:
* No credentials are hardcoded
* No .env files used
* Authentication is handled via IAM Role

## IAM Role — Least Privilege

Permission	         | Granted	| Reason

GetSecretValue.    	 | ✅ Yes    |Required to read secret
DescribeSecret	     |  ✅ Yes.  |	Required for metadata
Access to all secrets	 |  ❌ No	|Restricted to one ARN
Delete secret	     |  ❌ No	|Not needed
IAM permissions	     |  ❌ No	|Not required

## Secret Rotation (Manual)

Secret rotation was simulated manually using:
aws secretsmanager put-secret-value \
  --secret-id lab/m8-05/db-credentials \
  --secret-string file://rotated-secret.json
Before Rotation:
In***************1!
After Rotation:
Ro***************2!
Key Insight:
The application automatically reads the updated value without restart or redeployment, because it fetches the secret at runtime.

## Security Improvements

❌ Before
password = "SuperSecretPassword123!"
✅ After
creds = get_db_credentials("lab/m8-05/db-credentials")
password = creds["password"]

## Benefits:
* No credentials in source code
* No risk of leaking secrets in Git
* Centralized secret management
* Easy rotation

## Screenshots
Located in /screenshots:
* secret-created.png
* app-output-before-rotation.png
* app-output-after-rotation.png

## Key Takeaways
* IAM Roles remove the need for access keys
* Secrets Manager enables secure storage of credentials
* Applications should fetch secrets at runtime
* Rotation works seamlessly when secrets are not cached


## Resources Created
* Secret: lab/m8-05/db-credentials
* IAM Policy: lab-m8-05-secret-access
* IAM Role: lab-m8-05-ec2-role
* Instance Profile: lab-m8-05-instance-profile
* EC2 Instance: Amazon Linux 2 (t2.micro)

## Cleanup (Important)
To avoid charges:
aws ec2 terminate-instances --instance-ids <INSTANCE_ID>

aws secretsmanager delete-secret \
  --secret-id lab/m8-05/db-credentials \
  --recovery-window-in-days 7

## Conclusion
This lab demonstrates a production-grade pattern for secure secret management using AWS services. By combining Secrets Manager, IAM roles, and runtime retrieval, we eliminate common security risks associated with hardcoded credentials.


## Verification Checklist

- [ ✅ ] Secret stored in Secrets Manager
- [ ✅ ] Application retrieves secret successfully
- [ ✅ ] Rotation configured (or documented why not applicable)
- [ ✅ ] No hardcoded credentials in code

**Good luck! 🔒**
