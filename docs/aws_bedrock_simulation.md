# AWS Bedrock — SIMULATED (no AWS account required)

> SIMULATED SCREEN — NO AWS ACCOUNT REQUIRED.

## What real Bedrock does
Hosts the LLM. You call `invoke_model` with a model id and a prompt; it returns text.

## Where it sits
`context_builder.py` -> **bedrock_llm_service.generate()** -> answer -> `citation_service.py`.

## Mock request / response (local)
```json
// request  (context string built by context_builder.py)
{ "messages": [{ "role": "user", "content": "You are BidIntel... EVIDENCE: [1]..." }] }
// response (mock)
{ "answer": "Based on the retrieved evidence: ... [1]", "model": "mock-claude" }
```

## Production swap (one function body)
1. Console: **Bedrock > Model access** -> enable the model.
2. Ensure the task role has `bedrock:InvokeModel`.
3. Set `BEDROCK_MODEL_ID` (Secrets Manager).
4. Replace the mock branch in `bedrock_llm_service.py` with the real `boto3` call.
Nothing else in the pipeline changes.
