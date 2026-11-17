# NIAT Parent Decision Lens

**Growth Hack Challenge Round 1 | NxtWave Jr. Growth Manager (AI, Experiments & Community)**  
**Candidate:** Kalash (B.Tech, NIT Raipur)  
**Track:** Track A (Top of Funnel Parent Acquisition & Decision Clarity)  
**Avenue:** Regional College Fee & ROI Decision Tool with Verified UGC Accreditation Lookup  
**Live Production URL:** [https://niat-parent-lens.onrender.com](https://niat-parent-lens.onrender.com)  
**Repository:** [https://github.com/kalashkj28/niat-parent-lens](https://github.com/kalashkj28/niat-parent-lens)

---

## 1. System Overview
NIAT Parent Decision Lens is a multi-component growth system designed to resolve the primary conversion friction in NIAT's funnel: **parent fee bifurcation shock and degree validity skepticism**.

Instead of capturing leads with generic career ads and forcing cold tele-counselling calls, the system offers an interactive, transparent decision comparator in **Telugu, Hindi, and English**. Parents input entrance scores and family budgets to receive an unvarnished 4-year financial breakdown, UGC accreditation proof, and an AI-drafted parent advisory memo before speaking with sales agents.

---

## 2. Component Architecture & Connections

```
[ FRONTEND CLIENT ]
(Interactive Web Portal: index.html + app.js + styles.css)
        │
        ├── Multilingual Switcher (Telugu, Hindi, English)
        ├── Dynamic Fee Breakdown & Career ROI Payback Charts
        ├── UGC Accreditation Gazette Proof Dossier
        └── Live Growth Analytics Funnel & Feedback Dashboard
        │
        ▼ (HTTP REST API: port 8080)
[ BACKEND ORCHESTRATION SERVER ] (backend/server.py)
        │
        ▼
[ AI AGENT ORCHESTRATOR ] (backend/agent.py)
        ├── Tool 1: calculate_comparative_roi() (backend/tools.py)
        │     └── 4-Year Tuition, Upskilling, Hostel & Payback Math
        ├── Tool 2: verify_ugc_accreditation() (backend/tools.py)
        │     └── Public Regulatory Registry (Chalapathi, GMRIT, ADYPU)
        └── Tool 3: qualify_and_route_lead() (backend/tools.py)
              └── Intent Scoring, Objection Tagging & Human Escalation Triggers
        │
        ▼
[ VERNACULAR GENERATION & ROUTING ENGINE ]
        └── Synthesizes Tool Outputs into Respectful Native Memo
        │
        ▼
[ PERSISTENCE & AUDIT STORE ] (backend/db.py -> growth_engine.db)
        ├── Table: leads (contact, budget, scores, routing)
        ├── Table: interactions (audit trail of tool executions & latencies)
        └── Table: feedback_loop (counsellor dispositions & learning loop)
        │
        ▼
[ LEARNING LOOP CALIBRATOR ] (backend/learning_loop.py)
        └── Recalibrates Qualification Multipliers from Real Closing Rates
```

---

## 3. Tool Specifications & Failure Behavior

| Component / Tool | Inputs | Outputs | Failure & Fallback Behavior |
| :--- | :--- | :--- | :--- |
| **Tool 1: `calculate_comparative_roi`** | Board %, Entrance Rank, Budget, Hostel Need, Partner Campus | 4-Year net outlay, scholarship deduction, salary delta, payback months | Falls back to regional median benchmarks with labeled estimates |
| **Tool 2: `verify_ugc_accreditation`** | Partner Campus Name | UGC status, NAAC grade, AICTE approval, UPSC/GATE eligibility | Returns State Private University registry lookup link |
| **Tool 3: `qualify_and_route_lead`** | Lead profile, budget check, user notes | Intent score (1-100), priority tier, routing destination, human escalation flag | Assigns default `MEDIUM` priority and routes to General Admissions |
| **Vernacular Generator** | Synthesized agent payload, language (`te`/`hi`/`en`) | Respectful parent memo in native script | Falls back to plain English with direct WhatsApp contact button |
| **Human Escalation Trigger** | Free-text notes matching distress/dispute keywords | Immediate halt of sales automation; routing to Academic Dean | Displays transparent notice; disables automated dialing queue |

---

## 4. How to Run Locally

### Prerequisites
- Python 3.10+ (Tested on Python 3.12 with standard libraries)
- Modern web browser (Chrome, Edge, Firefox, Safari)
- Zero external package installation required (runs on built-in libraries)

### Step 1: Run the Agent CLI Test Suite
Verify that all tools, edge cases, and audit logging work in your terminal:
```bash
python backend/test_agent.py
```
Expected output: 7 passed tests (`OK`).

### Step 2: Seed Initial Testing Cohort (Optional)
Populate the 14 real user test records from the Raipur cohort:
```bash
python backend/reset_and_seed_clean_db.py
```

### Step 3: Start the Production HTTP Server
```bash
python backend/server.py
```
The server will start on `http://localhost:8080`.

### Step 4: Open the Application
Navigate in your browser to:
```
http://localhost:8080/
```
- Toggle between **English**, **తెలుగు (Telugu)**, and **हिन्दी (Hindi)**.
- Test the **Parent Decision Tool** with custom scores and budgets.
- Switch to the **Growth Analytics Dashboard** tab to view live funnel metrics, lead logs, and update the admissions learning loop.

---

## 5. Environment Variables & Security
- **No API keys in repository**: The core engine operates with zero hardcoded keys.
- If connecting Google Gemini API for live custom LLM generation, set:
  ```bash
  export GEMINI_API_KEY="your-gemini-api-key"
  ```
  If unset, the system uses the deterministic template generator with verified public data.
- **Privacy & Compliance**: Respects minimal data collection. No personal scraping. All candidate institutions are queried from public regulatory disclosures.
