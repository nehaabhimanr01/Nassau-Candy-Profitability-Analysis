# Nassau Candy Profitability Analysis

## 📊 Project Overview

This project analyzes the profitability performance of Nassau Candy Distributor using sales, cost, gross profit, product, division, region, and order-level data.

The objective is to identify revenue and profit drivers, evaluate product-level margins, detect low-margin products, and provide actionable business insights through an interactive Streamlit dashboard.

---

## 🎯 Business Objectives

- Analyze overall sales and gross profitability.
- Measure profit margins across products and divisions.
- Identify the highest and lowest-performing products.
- Understand profit concentration across the product portfolio.
- Detect products with low profitability and potential margin risk.
- Provide an interactive dashboard for business decision-making.

---

## 📁 Dataset

The analysis uses the **Nassau Candy Distributor** dataset containing **10,194 records and 18 columns**.

Key fields include:

- Sales
- Cost
- Gross Profit
- Units
- Division
- Product Name
- Region
- Order Date
- Ship Date
- Customer information

---

## 🛠️ Tools & Technologies

- **Python**
- **Pandas** – data cleaning and analysis
- **Plotly** – interactive visualizations
- **Streamlit** – interactive dashboard
- **GitHub** – project repository and version control

---

## 📈 Dashboard Features

The Streamlit dashboard provides:

### Key Performance Indicators
- Total Sales
- Gross Profit
- Overall Profit Margin
- Units Sold
- Number of Products

### Interactive Filters
- Division
- Region
- Order Date Range
- Product Search
- Minimum Profit Margin

### Analysis Modules
- Sales by Division
- Gross Profit by Division
- Top 10 Products by Gross Profit
- Product-level profitability table
- Lowest-margin products
- Cumulative profit / Pareto analysis
- Data quality checks
- Automated business insights

---

## 🔍 Key Findings

The analysis indicates:

- Total Sales: **$141,783.63**
- Gross Profit: **$93,442.80**
- Overall Profit Margin: **65.9%**
- Units Sold: **38,654**
- Products Analyzed: **15**

The analysis also highlights significant differences in profitability across products and divisions, with a small number of products contributing a substantial share of overall profit.

---

## 💡 Business Insights

The dashboard can help decision-makers:

- Focus attention on high-profit products.
- Investigate low-margin products for pricing or cost optimization.
- Understand which divisions contribute most to profitability.
- Monitor concentration risk within the product portfolio.
- Use interactive filtering to investigate specific products, regions, and periods.

---

## 🚀 Deployment

The project is deployed as an interactive **Streamlit web application**.

The deployed dashboard allows users to explore profitability metrics and business insights without requiring a local Python environment.

---

## 📂 Repository Structure

```text
Nassau-Candy-Profitability-Analysis/
│
├── Nassau_Candy_Profitability.csv
├── app.py
├── requirements.txt
└── README.md
