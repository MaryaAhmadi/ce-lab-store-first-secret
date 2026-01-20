# Lab M8.05 - Store First Secret in Secure System (Secrets Manager)

**Repository:** [https://github.com/cloud-engineering-bootcamp/ce-lab-store-first-secret](https://github.com/cloud-engineering-bootcamp/ce-lab-store-first-secret)

**Activity Type:** Individual  
**Estimated Time:** 45 minutes

## Learning Objectives

- [ ] Store secrets in AWS Secrets Manager
- [ ] Retrieve secrets from an application
- [ ] Configure automatic secret rotation
- [ ] Remove hardcoded credentials from code

## Prerequisites

- [ ] AWS account
- [ ] Python or Node.js installed locally
- [ ] RDS database (or mock credentials)
- [ ] Completed Module 8 Lesson 5

## Task

Migrate hardcoded database credentials to Secrets Manager, retrieve them in application code, and configure rotation.

## Step-by-Step Instructions

### Step 1: Create Secret

```bash
# Store database password
aws secretsmanager create-secret \
  --name prod/db/postgres \
  --description "Production PostgreSQL credentials" \
  --secret-string '{
    "username":"dbadmin",
    "password":"SuperSecretPassword123!",
    "host":"mydb.abc123.us-east-1.rds.amazonaws.com",
    "port":5432,
    "database":"myapp"
  }'
```

### Step 2: Retrieve Secret in Python Application

```python
# app.py
import boto3
import json

def get_secret():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId='prod/db/postgres')
    secret = json.loads(response['SecretString'])
    return secret

# Usage
db_creds = get_secret()
connection = psycopg2.connect(
    host=db_creds['host'],
    user=db_creds['username'],
    password=db_creds['password'],
    database=db_creds['database']
)
```

### Step 3: Configure Rotation

```bash
# Enable automatic rotation (30 days)
aws secretsmanager rotate-secret \
  --secret-id prod/db/postgres \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:SecretsManagerRotation \
  --rotation-rules AutomaticallyAfterDays=30
```

### Step 4: Test Retrieval

```bash
# Run application and verify it connects to database
python app.py
```

### Step 5: Remove Hardcoded Credentials

**Before (BAD):**
```python
password = "SuperSecretPassword123!"
```

**After (GOOD):**
```python
db_creds = get_secret()
password = db_creds['password']
```

## Submission

- Modified `app.py` with Secrets Manager integration
- Screenshot of secret in Secrets Manager
- Documentation of rotation configuration

## Verification Checklist

- [ ] Secret stored in Secrets Manager
- [ ] Application retrieves secret successfully
- [ ] Rotation configured (or documented why not applicable)
- [ ] No hardcoded credentials in code

**Good luck! 🔒**
