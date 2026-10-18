import httpx
import numpy as np
import json

API = "http://127.0.0.1:8000"

# Fetch run 4f8c89522501
r_data = httpx.get(f"{API}/v1/runs/4f8c89522501").json()
summary = r_data["summary"]
windows = r_data["windows"]
findings = r_data["findings"]
audit = httpx.get(f"{API}/v1/runs/4f8c89522501/audit").json()
steps = httpx.get(f"{API}/v1/runs/4f8c89522501/steps?after=-1").json()

# Signal beat confidences
sig = httpx.get(f"{API}/v1/runs/4f8c89522501/signal", params={"start_s": 0, "end_s": 300, "max_points": 3000}).json()
beats = sig.get("beats", [])
confidences = [b["confidence"] for b in beats if "confidence" in b]

stats = {
    "total_beats": summary["beats"],
    "classes": summary["classes"],
    "mean_sqi": summary["quality"]["mean_sqi"],
    "noise_median": summary["quality"]["noise_median"],
    "flat_frac": summary["quality"]["flat_frac"],
    "q_frac": summary["quality"]["q_frac"],
    "mean_confidence": float(np.mean(confidences)) if confidences else None,
    "min_confidence": float(np.min(confidences)) if confidences else None,
    "max_confidence": float(np.max(confidences)) if confidences else None,
    "total_windows_generated": len(windows),
    "total_windows_triaged": len(findings),
    "triaged_window_ids": sorted(findings.keys()),
    "audit_records_count": len(audit),
    "total_steps": steps["total"]
}

print(json.dumps(stats, indent=2))
with open("exact_numerical_stats.json", "w") as f:
    json.dump(stats, f, indent=2)
