import time
import httpx
import json

API = "http://127.0.0.1:8000"

print("--- Running CardioGuard Benchmark Suite ---")

# 1. Edge Case / Missing / Malformed
print("\n[Test C1] Missing Record Test")
r_missing = httpx.post(f"{API}/v1/runs", json={
    "record": "999_nonexistent", "start_s": 0.0, "duration_s": 300.0, "mode": "balanced", "scenario": None, "max_reviews": 6
})
print(f"Missing record response: Status={r_missing.status_code}, Detail={r_missing.json().get('detail')}")

print("\n[Test C2] Malformed Parameter Test (negative duration)")
r_malformed = httpx.post(f"{API}/v1/runs", json={
    "record": "233", "start_s": 0.0, "duration_s": -50.0, "mode": "balanced", "scenario": None, "max_reviews": 6
})
print(f"Negative duration response: Status={r_malformed.status_code}")

print("\n[Test C3] Stress Fault Scenario (clipped)")
t0 = time.time()
r_noise = httpx.post(f"{API}/v1/runs", json={
    "record": "233", "start_s": 0.0, "duration_s": 300.0, "mode": "balanced", "scenario": "clipped", "max_reviews": 6
})
print("Clipped run response status:", r_noise.status_code)
noise_run_id = r_noise.json()["id"]
for _ in range(40):
    time.sleep(1)
    status_data = httpx.get(f"{API}/v1/runs/{noise_run_id}").json()
    if status_data.get("status") in ("complete", "unreadable", "failed"):
        break
t_noise = time.time() - t0
print(f"Clipped scenario outcome: status={status_data.get('status')}, error={status_data.get('report', {}).get('error')}, latency={t_noise:.2f}s")

# 2. Performance & Replicability Benchmark
latencies = []
print("\n[Test B] Benchmarking runs on record 100 (normal/routine) and record 233 (ventricular arrhythmia)...")

for rec in ["100", "233"]:
    t_start = time.time()
    res = httpx.post(f"{API}/v1/runs", json={
        "record": rec, "start_s": 0.0, "duration_s": 300.0, "mode": "balanced", "scenario": None, "max_reviews": 6
    })
    rid = res.json()["id"]
    for _ in range(45):
        time.sleep(1)
        rdata = httpx.get(f"{API}/v1/runs/{rid}").json()
        if rdata.get("status") in ("complete", "unreadable", "failed"):
            break
    elapsed = time.time() - t_start
    findings = rdata.get("findings", {})
    windows_count = len(findings)
    window_keys = sorted(findings.keys())
    latencies.append({
        "record": rec,
        "run_id": rid,
        "status": rdata.get("status"),
        "tier": rdata.get("report", {}).get("overall_tier"),
        "windows_triaged_count": windows_count,
        "window_ids": window_keys,
        "total_time_s": round(elapsed, 2),
        "ms_per_window": round((elapsed / windows_count) * 1000, 1) if windows_count else None
    })
    print(f"Record {rec}: Status={rdata.get('status')}, Tier={rdata.get('report', {}).get('overall_tier')}, Windows count={windows_count}, Window IDs={window_keys}, Total Time={elapsed:.2f}s")

with open("benchmark_summary.json", "w") as f:
    json.dump({
        "edge_cases": {
            "missing_record_status": r_missing.status_code,
            "malformed_param_status": r_malformed.status_code,
            "clipped_fault_status": status_data.get("status"),
            "clipped_fault_error": status_data.get("report", {}).get("error"),
        },
        "performance": latencies
    }, f, indent=2)

print("\nBenchmark successfully completed and written to benchmark_summary.json")
