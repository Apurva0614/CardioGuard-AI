# CARDIOGUARD — Brand, Demo, Results & Verification Report

## 1. Project Overview and Objective
This project implements and evaluates the **CARDIOGUARD** system, an advanced architecture comprising two cooperating AI agents designed to pre-review long ambulatory ECG recordings (such as 24–72 hour Holter monitoring datasets) for clinician worklist prioritization. 

The primary clinical safety objective is deterministic: **a language model or downstream agent must never lower the urgency tier of a finding below the screening floor established by the signal perception classifier**. Damaged, unreadable, or noisy recordings are immediately flagged for human clinician review rather than triaged as routine.

---

## 2. Machine Specifications and Environment
- **Operating System:** Windows 11 Home Single Language (64-bit, Build 26100)
- **CPU Architecture:** x86_64 (AMD64)
- **System Memory:** 6.22 GB Total Physical RAM (~0.71 GB Free at initial inspection)
- **Storage:** Primary drive C:\ with >250 GB free disk space
- **Git Version:** 2.53.0.windows.2
- **Python Runtimes:** Python 3.12.10 (used for the isolated virtual environment `.venv`), Python 3.14.3 system default
- **Browser Automation:** Playwright 1.64.0 with headless Chromium (installed in `.venv`)

---

## 3. Actual Repository and App Entry Point
- **Repository URI / Git:** `c:\Users\dsatk\OneDrive\Documents\ecg-multi-agent-triage` (origin: `https://github.com/a1if/ecg-multi-agent-triage`)
- **Backend Service Entry Point:** `backend/src/ecg_agent/api/main.py` (FastAPI app served via Uvicorn on `http://127.0.0.1:8000`)
- **Streamlit Frontend Entry Point:** `frontend/app.py` (served via Streamlit on `http://127.0.0.1:8501`)
- **Combined Cloud/Local Runner:** `run_backend.py` + `frontend/app.py`

---

## 4. Branding and Attribution Changes
- **Application Presentation Name:** Standardized across all UI headers, browser title, sidebar, and page navigation as **`CARDIOGUARD`**.
- **Emoji Removal:** Unnecessary emojis removed across titles, navigation, metric badges, toast notifications, status icons, and conversational agent headers, resulting in a clean, professional clinical dashboard.
- **Streamlit Default Branding Hidden:** Embedded custom CSS to remove top header bar, hamburger menu, and "Hosted on Streamlit" footer.
- **Navigation Simplification:** Removed the "How it works" view from page navigation to focus directly on the Clinical Worklist and Recording triage interfaces.
- **UI Attribution Inspection & Handling:**
  - Audited `frontend/app.py`, `frontend/ui.py`, and `frontend/views/*.py`.
  - Confirmed the presentation name **CARDIOGUARD** is consistently applied without extraneous personal names or developer self-promotion.
  - Retained genuine academic research references outside presentation headers.
  - Retained all clinical safety disclaimers: *"Research prototype, not a medical device and not clinical advice."*


---

## 5. Setup Mode: FULL, PARTIAL, or MOCK/FALLBACK
- **Setup Mode:** **PARTIAL / REPLAY PRESET MODE** (`RECEIVER=replay`, `DEMO_PRESETS=1`).
- **Rationale:** 
  - Loading live Gemma 4 E4B weights with bitsandbytes NF4 quantization requires an NVIDIA CUDA GPU with ~12GB VRAM. The current local system is a CPU-only environment with 6.22 GB total RAM.
  - The repository officially supports a zero-GPU **replay preset mode**, which replays 985 verified, exact-number Gemma 4 E4B GPU inferences recorded on an RTX 5070 across MIT-BIH recordings.
  - The Perception Agent (CNN-LSTM on CPU), orchestrator state machine, deterministic guardrails, signal processing, and FastAPI/Streamlit pipelines all run 100% genuine local execution.

---

## 6. Succeeded and Failed Commands
### Succeeded Commands:
1. `py -3.12 -m venv .venv`: Created isolated Python 3.12 environment.
2. `.\.venv\Scripts\pip install -r requirements.txt`: Successfully compiled and installed dependencies (CPU PyTorch 2.11.0, NumPy, SciPy, Pandas, Streamlit, Plotly, HTTPX, and local `ecg-agent`).
3. `.\.venv\Scripts\pip install playwright pytest && .\.venv\Scripts\playwright install chromium`: Installed Playwright testing tools and Chromium browser.
4. `.\.venv\Scripts\python run_backend.py`: Successfully launched FastAPI backend API on `http://127.0.0.1:8000` with replay store (985 entries loaded).
5. `.\.venv\Scripts\streamlit run frontend/app.py`: Successfully launched Streamlit UI on `http://127.0.0.1:8501`.
6. `.\.venv\Scripts\python trigger_run.py`: Successfully scheduled, triaged, and evaluated MIT-BIH record 233.
7. `.\.venv\Scripts\python test_queries.py`: Successfully executed 6 test queries against the live orchestrator and safety guardrails.
8. `.\.venv\Scripts\python capture_all_shots.py`: Captured 8 full-page genuine screenshots with Playwright.

### Failed Commands / Errors Resolved:
1. `curl.exe -s -X POST http://127.0.0.1:8000/v1/runs -d '{"record":"233",...}'`: Escaping quotes in PowerShell caused a JSON parse error. Resolved by scripting requests via Python `httpx`.
2. Initial Playwright locator `summary:has-text('The agents\' conversation')`: Unescaped apostrophe in CSS selector triggered a Playwright parser error. Resolved by migrating to `page.get_by_text("The agents' conversation")`.

---

## 7. Verified Application Features
1. **Clinical Worklist (`/`):** Displays all patient recordings sorted by urgency tier (unreadable/faults first, then urgent, priority, routine).
2. **Interactive ECG Waveform & Annotations (`/run`):** Zoomable dual-lead signal plots with color-coded triage bands and beat-level classifications (N: normal, S: supraventricular, V: ventricular, F: fusion, Q: unclassifiable).
3. **Agent Conversation Trace (`/run`):** Real-time message exchange between Perception Agent, Orchestrator, Reasoning Agent, and Clinician.
4. **Channel Benchmarking (Adapter vs Filtered Text):** Side-by-side prompt token count, latency, and GPU energy comparison.
5. **Findings & Clinician Overrides:** Detailed window justifications, reference guideline facts, and clinician override form with permanent audit logging.
6. **Clinical Q&A & Two-Layer Guardrails:** Natural language question handling with strict refusal of medical advice and medication recommendations.
7. **System Architecture Graph (`/about`):** Visual Graphviz representation of agent roles, channels, and guardrails.

---

## 8. Results Table Location
The complete results table is saved at:
[`results/results_table.md`](results/results_table.md)

---

## 9. Screenshot Inventory
All 8 screenshots were captured via Chromium at 1440 × 900 resolution and are stored in `shots/`:
- [`shots/01_home.png`](shots/01_home.png) (84.5 KB) — Branded application homepage with clinical worklist rankings.
- [`shots/02_study_search.png`](shots/02_study_search.png) (123.3 KB) — ECG signal inspection with beat-level classification annotations.
- [`shots/03_drug_interactions.png`](shots/03_drug_interactions.png) (113.8 KB) — Clinician Q&A interface demonstrating guardrail refusals for medical/medication queries.
- [`shots/04_adverse_events.png`](shots/04_adverse_events.png) (58.0 KB) — Stress testing interface demonstrating signal fault scenarios (noise, clipping, electrode disconnects).
- [`shots/05_trial_comparison.png`](shots/05_trial_comparison.png) (116.2 KB) — Quantitative comparison of learned adapter virtual tokens vs filtered text.
- [`shots/06_graph_view.png`](shots/06_graph_view.png) (179.9 KB) — Multi-agent architecture diagram showing data flow and safety guardrails.
- [`shots/07_analytics.png`](shots/07_analytics.png) (101.4 KB) — Findings analytics, clinical guideline justifications, and override controls.
- [`shots/08_agent_trace.png`](shots/08_agent_trace.png) (121.5 KB) — Execution trace showing inter-agent communication and guardrail checks.

Gallery index: [`shots/index.html`](shots/index.html)

---

## 10. Five Concise Observations of the Interface & Workflow
1. **Urgency-First Worklist Sorting:** Unreadable recordings (e.g. noise/electrode dropouts) are elevated to the top of the queue because they require urgent human technician intervention rather than automated dismissal.
2. **Deterministic Safety Floor:** The reasoning agent is architecturally blocked by the orchestrator from downgrading any window below the tier computed by the CNN-LSTM perception agent.
3. **Rigid Clinical Guardrails:** When queried about clinical medication decisions (e.g. metformin, diabetes drugs, amiodarone), the system refuses advice immediately with a clear disclaimer before the LLM generates a response.
4. **Adapter Virtual-Token Efficiency:** On recordings with heavy arrhythmia burdens (such as record 233), the virtual-token adapter reduces prompt token load by up to 60% compared to verbose text listings.
5. **Transparent Source Attribution:** Every displayed finding, summary, and explanation explicitly reports its origin (*Gemma live*, *Gemma recorded answer*, or *deterministic rule*).

---

## 11. Agent Verification
- **Perception Agent (CNN-LSTM, CPU):** **Verified.** Processes raw ECG leads, computes signal-to-noise ratio, detects flatlines/clipping, classifies beats, and partitions windows.
- **Orchestrator (Deterministic Code):** **Verified.** Validates message schemas, enforces token budgets, checks guardrail invariants, and logs all events to the audit trail.
- **Reasoning Agent (Gemma 4 E4B / Replay):** **Verified.** Replays GPU inferences or evaluates rule-based logic to prioritize windows, justify classifications, and answer clinician questions.
- **Clinician Agent (Human-in-the-Loop):** **Verified.** Allows authorized clinicians to override classifications with an audit log reason.

---

## 12. Model, Dataset, and Backend Limitations
- **Not a Certified Medical Device:** This system is an academic research prototype evaluated on de-identified public datasets (MIT-BIH Arrhythmia Database).
- **Classifier Reliance:** The safety guardrail prevents LLM hallucination and under-triage, but it relies on the perception model's baseline sensitivity.
- **Replay Inference on Local CPU:** Live GPU generation requires high-memory CUDA environments; replay mode was used for this local demonstration.

---

## 13. Known Bugs and Recommended Next Steps
- **Cross-Platform Path Quoting:** When launching API and Streamlit services on Windows PowerShell, path variables and inline JSON payloads should be passed via scripts or JSON files to avoid shell string escaping issues.
- **Recommended Next Steps:** Integrate automated batch processing for multi-lead 12-lead Holter datasets and extend Docker Compose profiles for seamless deployment on cloud Kubernetes/Cloud Run environments.
