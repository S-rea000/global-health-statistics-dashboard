# Global Health Monitoring Dashboard

> **An interactive data visualization dashboard tracking global health outcomes across 20 countries and 6 regions (2000–2024), built with Python and Streamlit.**

---
## Live Demo
[Click here to view the dashboard](#)

---

## ⚠️ IMPORTANT — SYNTHETIC DATASET NOTICE

> [!WARNING]
> **THIS DASHBOARD USES SYNTHETIC (AI-GENERATED) DATA.**
> The dataset was algorithmically generated for educational and practice purposes only.
> **Values, statistics, and trends do NOT represent real-world health data.**
> Do not use this for medical, policy, or research decisions.

| | Details |
|---|---|
| **Dataset source** | Kaggle — malaiarasugraj (`global_health_statistics.csv`) |
| **Nature** | AI-generated / Synthetically simulated |
| **Purpose** | Educational data visualization practice |
| **Real data?** | ❌ No |

---

## Dashboard Features

- **Interactive choropleth world map** — health burden by country
- **KPI cards** — mortality, access, recovery, prevalence with trend indicators
- **Time-series trend analysis** — 2000–2024 with rolling averages
- **Disease burden distribution** — donut chart by disease category
- **Regional comparisons** — stacked bar & horizontal bar charts
- **Scatter plot** — prevalence vs mortality by region
- **Box plot** — treatment access gap distribution
- **Dynamic filters** — region, year range, disease category, map metric

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)

---

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/S-rea000/global-health-dashboard.git
cd global-health-dashboard

# 2. Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
streamlit run dashboard_app.py
```

---

## Project Structure

```
global-health-dashboard/
├── dashboard_app.py          # Main Streamlit app
├── data/
│   └── global_health_statistics.csv   # Synthetic dataset
├── requirements.txt
└── README.md
```

---

## Dataset Details

| Field | Info |
|---|---|
| Source | [Kaggle — Global Health Statistics](https://www.kaggle.com/) |
| Author | malaiarasugraj |
| Rows | ~1,000,000 |
| Countries | 20 |
| Year range | 2000–2024 |
| **Nature** | **⚠️ Synthetically generated — NOT real WHO/World Bank data** |

### Why synthetic?
The Kaggle dataset was programmatically generated to simulate global health patterns for learning and visualization practice. Key indicators like mortality rates show unrealistic uniformity across all diseases and countries — a clear sign of synthetic generation. COVID-19 records also appear pre-2019 in the raw data (removed during cleaning).

---

## Disclaimer

This project is built **entirely for learning purposes**.
All health statistics displayed are **synthetic and do not reflect reality**.
Not intended for clinical, policy, or research use.
