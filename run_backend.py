import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

os.environ["RECEIVER"] = "replay"
os.environ["DEMO_PRESETS"] = "1"
os.environ["CLASSIFIER"] = "gemma"
os.environ["ALLOW_UPLOADS"] = "0"
os.environ["RUNS_PER_MINUTE"] = "60"
os.environ["QUESTIONS_PER_MINUTE"] = "120"
os.environ["MAX_STORED_RUNS"] = "50"
os.environ["RECORDS_DIR"] = str(ROOT / "backend/data/records")
os.environ["MODELS_DIR"] = str(ROOT / "backend/artifacts/models")
os.environ["REPLAY_STORE"] = str(ROOT / "backend/data/replay/answers.jsonl")
os.environ["AUDIT_DIR"] = str(ROOT / "logs/audit")

import uvicorn
from ecg_agent.api.main import create_app
from ecg_agent.api.settings import Settings

app = create_app(Settings.from_env())
uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
