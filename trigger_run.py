import httpx
import json
import time

API = "http://127.0.0.1:8000"

print("Creating run for record 233...")
r = httpx.post(f"{API}/v1/runs", json={
    "record": "233",
    "start_s": 0.0,
    "duration_s": 300.0,
    "mode": "balanced",
    "scenario": None,
    "max_reviews": 6
}, timeout=60.0)
print("Create run response:", r.status_code, r.text)
run_data = r.json()
run_id = run_data["id"]
print(f"Run ID: {run_id}, status: {run_data.get('status')}")

# Poll until complete
for i in range(60):
    time.sleep(2)
    s = httpx.get(f"{API}/v1/runs/{run_id}", timeout=10.0).json()
    st = s.get("status")
    print(f"Polling run {run_id}: status={st}")
    if st not in ("queued", "running"):
        print("Run finished!")
        print("Findings count:", len(s.get("findings", {})))
        print("Overall tier:", (s.get("report") or {}).get("overall_tier"))
        break

# Test a question
print("Asking a question about the run...")
q_res = httpx.post(f"{API}/v1/runs/{run_id}/questions", json={"question": "Why is this recording marked urgent?"}, timeout=30.0)
print("Question answer:", q_res.status_code, q_res.json())

# Test a comparison
findings = s.get("findings", {})
if findings:
    wid = sorted(findings.keys())[0]
    print(f"Comparing channels for window {wid}...")
    cmp_res = httpx.post(f"{API}/v1/runs/{run_id}/windows/{wid}/compare", timeout=30.0)
    print("Compare result:", cmp_res.status_code, cmp_res.json())

    print(f"Explaining finding for window {wid}...")
    exp_res = httpx.post(f"{API}/v1/runs/{run_id}/windows/{wid}/explain", timeout=30.0)
    print("Explain result:", exp_res.status_code, exp_res.json())
