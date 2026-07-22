# 🌍 ClimateGuardian AI

**Community Climate Intelligence** — an AI-powered climate resilience platform for Nigerian communities, built for the **Build with Gemma: GenAI for SDGs** hackathon (Kwara State University).

> Early, community-verified reporting turns local observations into real-time risk intelligence — helping communities detect, respond to, and recover from climate and environmental hazards before they escalate.

---

## 🎯 SDG Alignment

- **SDG 11 — Sustainable Cities and Communities**: Strengthens local capacity for inclusive, community-driven disaster risk management by putting reporting and verification directly in residents' hands.
- **SDG 13 — Climate Action**: Builds adaptive capacity and early-warning infrastructure for climate-related hazards in communities that are otherwise underserved by formal monitoring systems.

---

## 👥 Who It's For

| Role | Use Case |
|---|---|
| 🌱 Crop Farmers | Report crop disease, drought, pest infestation |
| 🐄 Livestock/Poultry Farmers | Report livestock disease, heatwave impact |
| 🐟 Fish Farmers | Report fish pond issues, water quality problems |
| 🏠 Community Residents | Report flooding, erosion, infrastructure damage |

---

## ✨ Features

- **Authentication & Profiles** — registration with State → LGA → Community selection, secure bcrypt password hashing, security-question password recovery
- **Incident Reporting** — structured reports (type, severity, description, photo evidence) tied to exact location
- **Community Verification** — Confirm / False / Unsure voting on reports, with one vote per user per report enforced at the database level
- **Trust Scoring** — reporter trust score and badge, computed from how often their reports are community-verified
- **Live Community Risk Monitor** — a real-time risk score derived from report volume and severity
- **Government-Style Safety Advisories** — auto-generated guidance based on current risk level, multilingual-ready (English / Yoruba / Hausa / Igbo)
- **Live Weather Integration** — current conditions via Open-Meteo, factored into advisories
- **Incident Analytics** — severity and category breakdowns via interactive charts
- **Community Discussion** — comments on individual reports
- **Offline AI Assistant (Gemma)** — on-device reasoning for advisory generation and a community chat assistant *(integration completed live at the hackathon — see [Gemma Integration Status](#-gemma-integration-status) below)*

---

## 🛠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python
- **Database**: SQLite
- **Charts**: Plotly
- **Weather Data**: [Open-Meteo API](https://open-meteo.com/)
- **AI**: Gemma (running locally, offline)

---

## 📁 Project Structure

```
ClimateGuardianAI/
├── app.py                     # Entry point & routing
├── seed_demo_data.py          # Populates realistic demo data
├── requirements.txt
├── data/
│   └── nigeria_locations.json # State → LGA → Community hierarchy
├── database/
│   ├── database.py            # Schema + connection
│   ├── users.py                # Auth, profile, settings
│   ├── reports.py              # Incident CRUD + stats
│   ├── verifications.py        # Community voting
│   └── comments.py             # Report discussion
├── services/
│   ├── risk_engine.py          # Risk score calculation
│   ├── advisory_engine.py      # Safety advisory generation
│   ├── trust_engine.py         # Trust score & badges
│   └── weather.py              # Live weather integration
├── utils/
│   ├── auth.py                 # Login/register/logout pages
│   └── helpers.py              # Location data loading
└── views/
    ├── dashboard.py
    ├── report.py
    ├── community.py
    ├── assistant.py
    └── settings.py
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <https://github.com/Aceda-man/ClimateGuardianAI>
cd ClimateGuardianAI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database

```bash
python database/database.py
```

### 5. (Optional) Seed realistic demo data

```bash
python seed_demo_data.py
```

Demo login after seeding: `amara.demo@climateguardian.ai` / `DemoPass123!`

### 6. Run the app

```bash
streamlit run app.py
```

---

## 🤖 Gemma Integration Status

Gemma is being connected live during the hackathon (per event rules — frontend and supporting logic are built ahead of time, but the model setup itself happens on-site). Until then:

- `services/advisory_engine.py` uses a deterministic, rule-based advisory generator as a working baseline, so the app is fully functional without Gemma.
- Once integrated, Gemma will take over both:
  1. **Pattern interpretation** — turning report data + weather into more nuanced, context-aware advisories than the fixed threshold rules currently provide.
  2. **Community chat assistant** — answering user questions on-device, offline, in `views/assistant.py`.

---

## 🗣 Language Support

The Settings page lets users select English, Yoruba, Hausa, or Igbo. Advisory messages are currently translated for all four; further UI translation is planned. *(Note: non-English strings are machine-drafted and pending native-speaker review.)*

---

## 🔒 Environment & Security Notes

- No API keys are required — Open-Meteo's weather API is used without authentication.
- Passwords and security answers are hashed with `bcrypt`, never stored in plaintext.
- `database/climate.db` and `uploads/` are excluded from version control (see `.gitignore`) — they contain user data and should never be committed.

---

## 📄 License

Built for the Build with Gemma: GenAI for SDGs hackathon, Kwara State University.