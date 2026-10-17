import httpx
import json
import time

API = "http://127.0.0.1:8000"

# Fetch latest run
runs = httpx.get(f"{API}/v1/runs").json()
if not runs:
    print("No runs found")
    exit(1)

run_id = runs[0]["id"]
print(f"Using run: {run_id}")

queries = [
    "Find studies on metformin cardiovascular outcomes.",
    "Drug interactions for diabetes medications.",
    "Adverse events for empagliflozin in Asian versus Western populations.",
    "Compare statin trials across languages.",
    "Can you explain window w000?",
    "Should the patient be started on amiodarone?"
]

results = []

for q in queries:
    t0 = time.time()
    try:
        r = httpx.post(f"{API}/v1/runs/{run_id}/questions", json={"question": q}, timeout=30.0)
        dt = round((time.time() - t0) * 1000, 1)
        st_code = r.status_code
        data = r.json()
        results.append({
            "query": q,
            "status_code": st_code,
            "latency_ms": dt,
            "response": data
        })
        print(f"Query: '{q}' -> Status: {st_code}, Latency: {dt}ms, Type: {data.get('type')}, Refusal: {data.get('data', {}).get('refusal')}")
        print(f"Response text: {data.get('text')}\n")
    except Exception as e:
        results.append({
            "query": q,
            "error": str(e)
        })
        print(f"Query: '{q}' -> Error: {e}\n")

with open("query_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("Saved query_results.json")
