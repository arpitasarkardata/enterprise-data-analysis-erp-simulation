# 🛒 Enterprise Data Analysis & ERP Module Simulation
### End-to-End Data Analytics Project | 100K+ Orders E-Commerce Dataset

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql&logoColor=white)](https://mysql.com)
[![pandas](https://img.shields.io/badge/pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![matplotlib](https://img.shields.io/badge/matplotlib-Visualisation-11557C)](https://matplotlib.org)

---

## 📌 Overview

End-to-end analysis of a 100K+ order e-commerce dataset using SQL and Python. Includes automated data ingestion to MySQL, analytical queries with joins and window functions, and visualisations in pandas, matplotlib, and seaborn to uncover revenue trends, customer behaviour, and product insights.

This project simulates how an ERP system processes and reports on transactional data across Sales, Customer, Product, and Logistics modules — following the complete data analytics workflow from raw CSV ingestion to business insight generation.

---

## 🗂 Project Structure

~~~
enterprise-data-analysis-erp-simulation/
│
├── csv_to_mysql.ipynb          ← Automated CSV to MySQL data ingestion pipeline
├── ecommerce_sql_python.ipynb  ← 12 SQL analytical queries with Python visualisations
└── ecommerce_ppt.pptx          ← Business presentation of findings
~~~

---

## 🗄 Dataset

**e-Commerce Sales Dataset** — 100,000+ real e-commerce orders across 7 tables

| Table | Description |
|---|---|
| orders | Order records with status and timestamps |
| customers | Customer location and identity data |
| order_items | Line items with price and freight values |
| products | Product catalogue with category information |
| sellers | Seller location data |
| payments | Payment method and instalment details |
| geolocation | Geographic coordinates by zip code |

---

## ⚙️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Data loading, analysis, and visualisation |
| MySQL | Relational database storage and querying |
| pandas | Data manipulation and transformation |
| matplotlib / seaborn | Charts and visualisations |
| mysql-connector-python | Python to MySQL connectivity |

---

## 📊 Analytical Questions Covered

1. Revenue trend analysis by month and year
2. Top performing product categories by sales
3. Customer order frequency and behaviour
4. Seller performance ranking using window functions
5. Payment method distribution analysis
6. Order status breakdown and delivery performance
7. Year-over-year revenue growth calculation
8. Customer retention and repeat purchase rate
9. Regional sales concentration by state
10. Average order value by product category
11. Freight cost analysis by region
12. Cumulative revenue tracking with window functions

---

## ▶️ How to Run

**Step 1 — Clone the repository**
~~~bash
git clone https://github.com/arpitasarkardata/enterprise-data-analysis-erp-simulation.git
cd enterprise-data-analysis-erp-simulation
~~~

**Step 2 — Install dependencies**
~~~bash
pip install pandas mysql-connector-python matplotlib seaborn
~~~

**Step 3 — Set up MySQL**
~~~bash
mysql -u root -p -e "CREATE DATABASE ecommerce;"
~~~

**Step 4 — Run the ingestion notebook**
~~~
Open csv_to_mysql.ipynb in Jupyter Notebook
Update MySQL credentials in Cell 1
Kernel → Restart & Run All
~~~

**Step 5 — Run the analysis notebook**
~~~
Open ecommerce_sql_python.ipynb in Jupyter Notebook
Kernel → Restart & Run All
~~~

---

*Built by Arpita Sarkar — B.Tech ECE, Kalyani Government Engineering College (MAKAUT), 2025*
*GitHub: [arpitasarkardata](https://github.com/arpitasarkardata) | LinkedIn: [linkedin.com/in/arpita-sarkar-00921a225](https://www.linkedin.com/in/arpita-sarkar-00921a225/)*
