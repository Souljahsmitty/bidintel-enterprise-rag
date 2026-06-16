"""Cost + latency monitoring: record latency, token estimates, and an estimated cost
for every request into request_logs."""
import time

# rough local estimate; production reads real token counts + price from the model API
COST_PER_1K_IN = 0.003
COST_PER_1K_OUT = 0.015

class Timer:
    def __enter__(self): self.t0 = time.time(); return self
    def __exit__(self, *a): self.ms = int((time.time() - self.t0) * 1000)

def estimate_cost(in_tokens, out_tokens):
    return round(in_tokens / 1000 * COST_PER_1K_IN + out_tokens / 1000 * COST_PER_1K_OUT, 6)

def log_request(cur, tenant_id, endpoint, latency_ms, in_tokens=0, out_tokens=0):
    try:
        cur.execute("""INSERT INTO request_logs
            (tenant_id,endpoint,latency_ms,input_tokens,output_tokens,estimated_cost)
            VALUES (%s,%s,%s,%s,%s,%s)""",
            (tenant_id, endpoint, latency_ms, in_tokens, out_tokens,
             estimate_cost(in_tokens, out_tokens)))
    except Exception:
        pass
