"""Phoenix tracing wrapper. SIMULATED locally: records named spans in memory and logs
them, so the pipeline path is visible with no external service. In production, install
arize-phoenix + openinference and replace _emit() with real span export."""
import time, json

def trace(stage: str, data=None):
    _emit({"stage": stage, "t": time.time(), "data": data})

def _emit(span):
    # SIMULATED: print a compact trace line. Production: export to Phoenix.
    try:
        print("PHX", json.dumps(span, default=str)[:300])
    except Exception:
        pass
