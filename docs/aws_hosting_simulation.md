# AWS Hosting — SIMULATED (no AWS account required)

> SIMULATED SCREEN — NO AWS ACCOUNT REQUIRED.

## Local Docker  ->  AWS production (same shape)
```
docker-compose service   ->  AWS service
db (pgvector)            ->  Amazon RDS for PostgreSQL (+ pgvector)
backend (FastAPI image)  ->  Amazon ECR -> ECS Fargate (wears bidintel-task-role)
frontend (React build)   ->  S3 + CloudFront
(login)                  ->  Amazon Cognito user pool
(env vars)               ->  AWS Secrets Manager
```

## Production diagram
```
Users -> CloudFront + S3 (React) -> ALB -> ECS Fargate (backend)
                                            -> RDS Postgres + pgvector
                                            -> Bedrock (LLM)
```

## Deploy order (only AFTER the local loop works)
1. `docker build` + push backend image to ECR.
2. Create IAM task role (see aws_iam_simulation.md).
3. Store secrets in Secrets Manager.
4. Create RDS (enable pgvector), run create_tables.sql.
5. Create ECS service + ALB; point image at ECR tag.
6. Build React, upload to S3, front with CloudFront.
7. Create Cognito user pool; wire Login.jsx production branch.
8. Enable Bedrock model; flip `BEDROCK_MODEL_ID`.
