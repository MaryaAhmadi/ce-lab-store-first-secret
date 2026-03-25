# Lab M8.05 Report — EC2 App with Secrets Manager

## Architecture Summary

In this lab, I created a secret in AWS Secrets Manager named `lab/m8-05/db-credentials` that stores fictional database connection details including username, password, host, port, and database name. I then created an IAM policy with least-privilege access that allows only `GetSecretValue` and `DescribeSecret` on that one specific secret ARN, and nothing broader. An EC2 instance was launched with an attached IAM role through an instance profile, so the application could authenticate to AWS without storing access keys on the server. The Python application used boto3 to call Secrets Manager at runtime and retrieve the latest version of the secret dynamically.

## IAM Role: Least Privilege Analysis

| Permission | Granted? | Why |
|---|---|---|
| `secretsmanager:GetSecretValue` on this secret | ✅ Yes | Needed to read the secret |
| `secretsmanager:GetSecretValue` on all secrets | ❌ No | Only this secret ARN is allowed |
| `secretsmanager:DeleteSecret` | ❌ No | The app does not need to delete secrets |
| `iam:*` | ❌ No | The app does not need IAM administration permissions |

## Rotation Evidence

Before rotation:
- Password visible characters: `In***************1!`

After rotation:
- Password visible characters: `Ro***************2!`

## Reflection Questions

### 1. Why is an IAM role safer than putting `AWS_ACCESS_KEY_ID` in a `.env` file on the EC2 instance?

An IAM role is safer because AWS provides temporary credentials automatically through the EC2 instance metadata service, so no long-lived access keys need to be stored on disk or inside application files. If credentials are hardcoded in a `.env` file, they can be leaked through source control, backups, logs, or accidental file exposure. IAM roles also make it easier to enforce least privilege and rotate credentials automatically behind the scenes.

### 2. What would happen if the application cached the secret at startup and the secret was rotated?

If the application cached the secret only at startup, it would continue using the old credential even after the secret was rotated. That could cause authentication failures if the old password became invalid. To handle rotation safely, the application should either fetch the secret when needed, periodically refresh it, or implement cache invalidation with retry logic.

### 3. How would this pattern change if you needed to call Secrets Manager from a Lambda function instead of EC2?

With Lambda, there would be no EC2 instance profile. Instead, the Lambda execution role would be granted least-privilege access to the same secret. The Python code using boto3 would stay very similar, but the function would run inside Lambda and use the Lambda execution role automatically to authenticate to AWS.

## Resources Created

- Secret name: `lab/m8-05/db-credentials`
- Secret ARN: `arn:aws:secretsmanager:us-east-1:070638634202:secret:lab/m8-05/db-credentials-vcCaDr`
- IAM policy: `lab-m8-05-secret-access`
- IAM role: `lab-m8-05-ec2-role`
- Instance profile: `lab-m8-05-instance-profile`
- Working EC2 instance key pair: `ce-lab-logging`
