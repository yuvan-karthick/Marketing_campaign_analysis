# Retail Marketing Analytics — End-to-End Project

An end-to-end analytics solution to understand customer behavior, campaign performance, and high-value segments for a retail marketing dataset. The project covers **data cleaning → EDA → rule-based segmentation → SQL analytics → interactive dashboard (Streamlit)** and delivers actionable business recommendations.

---

## 🚀 Project Overview

**Objective**
Build a consolidated analytics solution to:

* Identify the most valuable and most responsive customer segments
* Understand spending behavior across products and channels
* Evaluate campaign effectiveness
* Detect under-served segments and propose actionable strategies

**Tech Stack**

* Python (Pandas, NumPy)
* SQL (SQLite)
* Streamlit (dashboard)
* Plotly / Matplotlib / Seaborn (visuals)

---

## 🗂 Project Structure

```
Marketing_campaign_analysis/
│
├── data/
│   ├── marketing_data.csv                # Raw data (unchanged)
│   ├── marketing_data_cleaned.csv        # Cleaned & feature-engineered data
│   ├── marketing_data_segmented.csv      # Segmented dataset
│   └── marketing_analytics.db            # SQLite analytical database
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb             # Cleaning + feature engineering
│   ├── 02_eda.ipynb                       # Exploratory Data Analysis
│   ├── 03_segmentation.ipynb              # Rule-based segmentation
│   ├── 04_sql_setup.ipynb                 # DB creation + data load
│   └── 05_sql_analytics.ipynb             # KPI & business SQL queries
│
├── streamlit_app.py                       # Interactive dashboard
└── README.md                              # This file
```

---

## 🔧 Setup Instructions

### 1️⃣ Create & Activate Virtual Environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 2️⃣ Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn plotly streamlit
```

---

## 🧹 Data Pipeline

### Step 1 — Data Cleaning & Feature Engineering

Notebook: `01_data_cleaning.ipynb`

Key operations:

* Convert `Dt_Customer` to datetime
* Create derived features:

  * `Age`
  * `Children`
  * `Total_Spend`
  * `Total_Purchases`
  * `Customer_Tenure_Days`
  * `Age_Band`, `Income_Band`
* Handle unrealistic ages and extreme income outliers

Output:

```
data/marketing_data_cleaned.csv
```

---

### Step 2 — Exploratory Data Analysis (EDA)

Notebook: `02_eda.ipynb`

Key analyses:

* Age, income, and spend distributions
* Response vs income and response vs spend
* Channel usage patterns
* Product category spending

Insights used later for segmentation and recommendations.

---

### Step 3 — Rule-Based Segmentation

Notebook: `03_segmentation.ipynb`

Segments created:

* High Spender
* High Income
* Campaign Responder
* High Web Engagement
* Family Customer
* Young Customer
* Standard Customer

Logic uses priority-based rules combining spend, income, response, engagement, age, and family composition.

Output:

```
data/marketing_data_segmented.csv
```

---

### Step 4 — SQL Data Modeling & Loading

Notebook: `04_sql_setup.ipynb`

* Create SQLite database: `marketing_analytics.db`
* Create main table: `customers`
* Load segmented dataset into SQL

This forms the **analytical backend** for dashboards and KPI queries.

---

### Step 5 — SQL Analytics

Notebook: `05_sql_analytics.ipynb`

Key KPIs and queries:

* Overall campaign response rate
* Response rate by customer segment
* Campaign-wise effectiveness (Cmp1–Cmp5)
* Segment-level value metrics (avg spend, avg income)
* Channel usage by segment
* Under-served segment detection (high engagement, low response)

---

## 📊 Running the Dashboard (Streamlit)

From the project root:

```bash
streamlit run streamlit_app.py
```

The dashboard provides:

* Overview KPIs
* Segment performance charts
* Campaign comparison
* Channel behavior analysis
* Under-served segment identification
* Filters by Country, Segment, Age Band, and Income Band

---

## 🔑 Key Findings

### Most Valuable Segments

* **High Spender**: Highest average spend (₹1953) and response rate (25.71%)
* **High Income**: Highest income group with strong response rate (22.15%)

### Most Responsive Segments

* High Spender and High Income customers are the best operational targets

### Under-Served Segment (Big Opportunity)

* **High Web Engagement** segment:

  * Largest customer group
  * Highest digital activity
  * 0% response rate
  * Low spending

---

## 🎯 Actionable Recommendations

1. **Prioritize High Spender customers** for premium and loyalty campaigns to maximize ROI.
2. **Target High Income customers** with personalized offers and premium product bundles.
3. **Redesign digital campaigns** for High Web Engagement customers using retargeting and personalization strategies.
4. **Focus campaign budget on Campaign 1 strategies** and redesign or discontinue Campaign 2 due to poor performance.
5. **Adopt omnichannel strategy** (store + web) for high-value segments.

---

## 🧠 How to Explain This Project (Viva / Interview Ready)

* *Pipeline*: Raw CSV → Cleaned Data → Segmentation → SQLite DB → SQL KPIs → Streamlit Dashboard
* *Why rule-based segmentation?* Transparent, business-aligned, easy to deploy in SQL and dashboards
* *Why SQLite?* Lightweight, serverless, perfect for analytical prototypes and dashboards
* *Business value*: Identifies high-value customers, optimizes campaign targeting, and reveals untapped digital opportunities

---

## 📌 Notes

* Raw data files are never modified
* All transformations are reproducible via notebooks
* Dashboard auto-refreshes based on filters

---

## ✅ Final Status

* Python & EDA: ✔ Complete
* Segmentation: ✔ Complete
* SQL Modeling & Analytics: ✔ Complete
* Dashboard: ✔ Complete
* Business Insights & Recommendations: ✔ Complete

---

**Author:** Yuvan
**Project:** Retail Marketing Analytics — End-to-End
