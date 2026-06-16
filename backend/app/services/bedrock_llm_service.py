"""MOCK Bedrock for local builds — no AWS account, no cost.
Same request/response shape as real Bedrock so production is a one-function swap."""
import os, re

def generate(context: str) -> dict:
    model = os.getenv("BEDROCK_MODEL_ID", "mock-claude")
    if model == "mock-claude":
        first = ""
        m = re.search(r"\[1\] \([^)]*\) (.+)", context)
        if m:
            first = m.group(1)[:200]
        answer = f"Based on the retrieved evidence: {first} [1]"
        return {"answer": answer, "model": model, "usage": {"in": 812, "out": 140}}
    # PRODUCTION branch (see docs/aws_bedrock_simulation.md):
    import boto3, json
    rt = boto3.client("bedrock-runtime")
    resp = rt.invoke_model(
        modelId=model,
        body=json.dumps({"messages": [{"role": "user", "content": context}]}),
    )
    out = json.loads(resp["body"].read())
    return {"answer": out["content"][0]["text"], "model": model}
