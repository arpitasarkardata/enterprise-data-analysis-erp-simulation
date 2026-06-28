# 🚀 GTM Business Intelligence Platform
### AI-Powered Go-To-Market Analytics | Enterprise E-Commerce Dataset (100K+ Orders)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Claude API](https://img.shields.io/badge/Claude-AI%20Insights-7C6AF7?logo=anthropic&logoColor=white)](https://anthropic.com)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql&logoColor=white)](https://mysql.com)

---

## 📌 Overview

This project builds a **GTM Business Intelligence Platform** — the kind of analytics infrastructure that supports Go-To-Market leadership teams at enterprise software companies. It combines a 100K+ order e-commerce dataset with an AI insight layer and conversational query engine to demonstrate the full BI stack.

**Three capabilities in one project:**

| Capability | What it does | JD Alignment |
|---|---|---|
| 📊 GTM KPI Dashboard | Revenue growth, customer retention, seller productivity, regional concentration | "Build robust metrics" |
| 🤖 LLM Insight Layer | Claude API generates executive-ready briefings from live data | "AI-powered quantitative insights" |
| 💬 Natural Language → SQL | Ask business questions in plain English → instant SQL + results | "Conversational intelligence tools" |

---

## 🎯 GTM KPIs Tracked

### Revenue KPIs
- **Month-over-Month Revenue Growth Rate** — trend line across 24 months
- **Year-over-Year Revenue Growth** — 2017 vs 2018 comparison
- **Category Revenue Concentration** — top 10 product categories by share
- **Cumulative Revenue Growth** — pipeline-style cumulative tracking

### Customer KPIs
- **Customer Retention Rate** — returning vs one-time buyer ratio
- **Churn Rate** — inverse of retention; early warning signal
- **New vs Returning Customer Trend** — monthly stacked view
- **Regional Customer Concentration** — top states by unique buyers

### Seller / Productivity KPIs
- **Seller Revenue Ranking** — DENSE_RANK() across all sellers
- **Seller Productivity Tiers** — High / Mid / Low based on revenue percentiles
- **Average Order Value by Seller** — productivity efficiency metric
- **Regional Revenue Penetration** — state-level revenue share

---

## 🤖 AI Features

### 1. LLM Insight Layer (Claude API)
After each KPI block, live data is passed to Claude to generate a structured executive briefing:
- 3 key insight bullets
- 1 risk flag
- 1 recommended GTM action

**Example prompt pattern:**
```
"You are a Senior GTM BI Analyst preparing a briefing for the VP of Sales.
Based on this data: [live KPI summary], generate a concise executive insight..."
```

### 2. Natural Language → SQL Engine
Type any business question in plain English — Claude converts it to MySQL and executes it against the database. No SQL knowledge required.

**Example queries:**
```
"Show me total revenue by customer state, top 5"
→ SELECT c.customer_state, ROUND(SUM(oi.price+oi.freight_value),2) AS revenue ...

"Who are the top 5 sellers by revenue?"
→ SELECT oi.seller_id, ROUND(SUM(oi.price+oi.freight_value),2) AS revenue ...

"What percentage of orders use credit card?"
→ SELECT payment_type, COUNT(*)*100.0/SUM(COUNT(*)) OVER() AS pct ...
```

This is the same principle behind **ThoughtSpot's SearchIQ** — built from scratch to demonstrate the underlying concept.

### 3. Prompt Engineering
System prompts used in this project are documented below — each is structured for a specific GTM use case:

| Prompt | Purpose | Output format |
|---|---|---|
| Revenue briefing | VP Sales weekly update | 3 bullets + risk + action |
| Retention alert | Customer Success VP | Diagnosis + root causes + interventions |
| Seller productivity | Sales Ops Head | Tier summary + warning + coaching tip |
| NL→SQL conversion | Any user | Raw MySQL query |

---

## 🛠 Tools & Technologies

| Tool | Purpose |
|---|---|
| Python | Data pipeline, analysis, API integration |
| MySQL | Database storage, Open SQL queries |
| pandas | Data manipulation and transformation |
| Claude API (Anthropic) | LLM insight generation, NL→SQL |
| Streamlit | Interactive BI dashboard |
| matplotlib / seaborn | Data visualisations |
| Cursor.ai | AI-assisted code development |

---

## 🗂 Project Structure

```
enterprise-data-analysis-erp-simulation/
│
├── gtm_bi_dashboard.ipynb        ← NEW: GTM KPIs + LLM insights + NL→SQL engine
├── streamlit_app.py              ← NEW: Interactive Streamlit BI dashboard
├── requirements.txt              ← NEW: All dependencies
│
├── ecommerce_sql_python.ipynb    ← Original: 12 SQL queries across ERP modules
├── csv_to_mysql.ipynb            ← Original: Automated CSV → MySQL ingestion pipeline
├── ecommerce_ppt.pptx            ← Original: Business presentation
└── README.md                     ← This file
```

---

## ▶️ How to Run

### Step 1 — Clone & Install
```bash
git clone https://github.com/arpitasarkardata/enterprise-data-analysis-erp-simulation.git
cd enterprise-data-analysis-erp-simulation
pip install -r requirements.txt
```

### Step 2 — Set up MySQL (if not already done)
```bash
# Create database
mysql -u root -p -e "CREATE DATABASE ecommerce;"

# Run the ingestion notebook first
jupyter notebook csv_to_mysql.ipynb
# Update credentials in Cell 1, then Kernel → Restart & Run All
```

### Step 3 — Set your Claude API key
```bash
# Get free key at: https://console.anthropic.com
export ANTHROPIC_API_KEY="your_key_here"
```

### Step 4 — Run the GTM BI Notebook
```bash
jupyter notebook gtm_bi_dashboard.ipynb
# Update DB credentials in Cell 2, then Kernel → Restart & Run All
```

### Step 5 — Launch Streamlit Dashboard
```bash
streamlit run streamlit_app.py
# Opens at http://localhost:8501
```

---

## 🗂 Dataset

**Brazilian Ecommerce Public Dataset** — 7 interconnected tables, 100,000+ records

| Table | Rows | GTM Equivalent |
|---|---|---|
| orders | ~100K | Sales pipeline / deal records |
| customers | ~100K | CRM contact records |
| order_items | ~115K | Line items / revenue breakdown |
| products | ~33K | Product catalogue |
| sellers | ~3K | Sales rep / partner records |
| payments | ~104K | Payment / billing data |
| geolocation | ~1M | Territory / regional master data |

Source: [Kaggle — Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

## 📊 Original ERP Analysis (Stage 1 & 2)

The original notebooks perform a 12-query ERP module analysis mapping the dataset to SAP SD / CRM / MM / FI module equivalents. See `ecommerce_sql_python.ipynb` for:
- Revenue reporting with window functions (DENSE_RANK, SUM OVER)
- Customer retention rate (double CTE + DATE_ADD)
- Year-over-year growth (CTE + LAG)
- Cumulative sales tracking
- Order volume heatmaps

---

*Built by Arpita Sarkar — B.Tech ECE, Kalyani Government Engineering College (MAKAUT), 2025*  
*GitHub: [arpitasarkardata](https://github.com/arpitasarkardata) | Contact: arpitasarkarkgec@gmail.com*  
*LinkedIn: [linkedin.com/in/arpita-sarkar-00921a225](https://www.linkedin.com/in/arpita-sarkar-00921a225/)*
