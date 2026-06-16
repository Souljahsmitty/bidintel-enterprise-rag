# AWS IAM — SIMULATED (no AWS account required)

> SIMULATED SCREEN — NO AWS ACCOUNT REQUIRED. These notes show what the real AWS
> screens would do and where they sit in production. Locally, none of this is needed.

## Users vs Roles vs Policies
- **Policy** = one permission ("can call bedrock:InvokeModel").
- **Role** = a bundle of policies a *service* temporarily wears (no stored passwords).
- **User** = a human identity (handled by Cognito for app login).

## Flow in production
```
User (Cognito) -> IAM Role (bidintel-task-role) -> Policies:
   bedrock:InvokeModel          (call the LLM)
   secretsmanager:GetSecretValue (read DB creds + model id)
   rds-db:connect               (connect to Postgres)
   logs:PutLogEvents            (write CloudWatch logs)
```

## Console steps that would matter (IAM > Roles > Create role)
1. Trusted entity: **ecs-tasks.amazonaws.com** (only ECS can assume it).
2. Attach the four least-privilege policies above.
3. Note the Role ARN; reference it as `taskRoleArn` in the ECS task definition.

## What is mocked locally instead
- No role. The backend reads `.env` directly and calls the **mock** Bedrock service.
- Swap happens only in `bedrock_llm_service.py` once `BEDROCK_MODEL_ID` is real.
