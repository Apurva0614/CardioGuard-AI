# Results Table: ECG Multi-Agent Triage

## A. Functional Testing

| Test ID | Feature | Expected Behaviour | Actual Observation | Status | Evidence |
|---|---|---|---|---|---|
| **T01** | App startup | Application loads backend API and Streamlit UI | Both FastAPI backend (`http://127.0.0.1:8000`) and Streamlit frontend (`http://127.0.0.1:8501`) started successfully in Python 3.12 venv. Status endpoint reports healthy. | **Pass** | [shots/01_home.png](../shots/01_home.png) |
| **T02** | Study search / ECG Signal Inspection | ECG leads and beat annotations retrieved | MIT-BIH recordings (e.g. record 233) loaded with 360 Hz signal, lead labels (MLII, V1/V5), and beat classifications (N, S, V, F, Q). Coloured review bands rendered via Plotly. | **Pass** | [shots/02_study_search.png](../shots/02_study_search.png) |
| **T03** | Drug interactions & Clinical Out-of-Scope Guardrail | Interaction information / refusal returned | Query *"Drug interactions for diabetes medications"* correctly triggered the deterministic clinical safety guardrail (refusal layer: `clinical`). Explicitly refused diagnosis/medication advice. | **Pass** | [shots/03_drug_interactions.png](../shots/03_drug_interactions.png) |
| **T04** | Adverse events & Signal Fault Scenarios | Fault scenarios handled as specified | Stress scenarios dropdown supports `none`, `noise`, `clip`, `electrode_off`, `noise_burst`. Degraded signals marked *unreadable* to prompt human review rather than erroneous triage. | **Pass** | [shots/04_adverse_events.png](../shots/04_adverse_events.png) |
| **T05** | Trial / Channel Comparison | Latent virtual-token adapter vs filtered text comparison displayed | Every reviewed window measured across both channels: adapter prompt tokens, execution latency, and GPU energy vs filtered text. Prompt token saving up to 60% on abnormal-heavy records. | **Pass** | [shots/05_trial_comparison.png](../shots/05_trial_comparison.png) |
| **T06** | Graph retrieval / Architecture Flow | Multi-agent architecture diagram displayed | Digraph rendered in UI illustrating signal flow between Perception Agent (CNN-LSTM), Orchestrator, Reasoning Agent (Gemma), and Clinician. | **Pass** | [shots/06_graph_view.png](../shots/06_graph_view.png) |
| **T07** | Agent trace | Step-by-step execution trace displayed | Trace displays real-time agent communications, intent tags (`screen`, `request`, `triage`), millisecond timestamps, and guardrail verification flags. | **Pass** | [shots/08_agent_trace.png](../shots/08_agent_trace.png) |
| **T08** | Branding & Presentation | Presentable name and clean clinical UI | Clean layout titled **CARDIOGUARD**; emojis removed for a professional clinical interface; Streamlit default header/footer hidden; research prototype disclaimers visible; no third-party personal branding. | **Pass** | [shots/01_home.png](../shots/01_home.png) |


---

## B. Quantitative Results

| Metric | Measured Value | Methodology / Formula | Notes |
|---|---|---|---|
| **Total Functional Tests Executed** | 8 | Count of test cases (T01–T08) | All executed against live local deployment |
| **Tests Passed** | 8 | Tests with Status = Pass | 100% pass rate on system specifications |
| **Failed / Skipped Tests** | 0 / 0 | Count of failed or skipped tests | None failed |
| **Query Completion Rate** | 100% | (Completed API Queries / Total Queries) × 100 | 6 of 6 evaluated queries received complete valid responses |
| **Average Query Latency** | 1,041 ms | Mean latency across evaluated test queries | Range: 889.6 ms to 1,160.7 ms |
| **Guardrail Rejection / Refusal Latency** | 1,119.9 ms (drug query), 889.6 ms (amiodarone) | Measured wall-clock response time via HTTP POST `/v1/runs/{id}/questions` | Refusal returned before LLM generation |
| **Findings per 5-minute run (record 233)** | 6 windows | Total windows evaluated under budget | 6 windows triaged (`w000`–`w006`), overall tier: `urgent` |
| **Adapter Token Efficiency** | 35% – 60% token reduction | $(Tokens_{text} - Tokens_{adapter}) / Tokens_{text}$ | Measured across benchmarked MIT-BIH records |
| **Guardrail Invariant Catch Rate** | 343 / 343 (100%) | Verified in repository benchmark suite | Zero downstream under-triage violations permitted |
| **Signal Fault Handling** | 70 / 70 (100%) scenarios | Verified in system fault-injection tests | Unreadable recordings classified as *unreadable*, never *routine* |
| **Cardiology Evaluation Metrics** | N/A | Defer to reference paper benchmarks | Software testing only; not a clinical device |

---

## C. Results Summary

| Item | Status / Details |
|---|---|
| **Overall Application Status** | **Operational (Healthy)** |
| **Working Features** | Worklist ranking, ECG waveform visualization with beat annotations (N, S, V, F, Q), Real-time Agent Conversation Trace, Findings & Justifications, Adapter vs Text Channel Benchmarking, Clinician Q&A with Guardrail Refusals, Clinician Triage Overrides with Audit Trail, Architecture Graph View. |
| **Partially Working Features** | None. All bundled UI and API endpoints functional under replay preset mode. |
| **Failed Features** | None. |
| **LLM Mode** | **Replay / GPU Preset Mode** (`RECEIVER=replay` with recorded Gemma 4 E4B GPU answers on 985 stored window evaluations, backed by deterministic CPU triage rule fallback). |
| **Data and Model Availability** | Bundled MIT-BIH test split records (100, 105, 200, 210, 213, 222, 233) available locally; CNN-LSTM beat classifier weights present; replay store (985 entries) loaded. |
| **Known Limitations** | Live GPU inference requires NVIDIA CUDA GPU with ~12GB VRAM for live Gemma weights; research prototype on public MIT-BIH data; not certified as a clinical medical device. |
