import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Nassau Candy Profitability Analysis",
    page_icon="🍫",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #17324D;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 16px;
        color: #5F6B7A;
        margin-bottom: 25px;
    }

    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .kpi-label {
        color: #64748B;
        font-size: 14px;
        font-weight: 600;
    }

    .kpi-value {
        color: #17324D;
        font-size: 28px;
        font-weight: 700;
        margin-top: 5px;
    }

    .section-title {
        color: #17324D;
        font-size: 23px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .insight-box {
        background-color: #EEF7F5;
        border-left: 5px solid #2A9D8F;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    file_path = "Nassau_Candy_Profitability.csv"
    df = pd.read_csv(file_path)

    # Convert dates
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True,
        errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        dayfirst=True,
        errors="coerce"
    )

    # Numeric columns
    for col in ["Sales", "Units", "Gross Profit", "Cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Profit margin
    df["Profit Margin %"] = (
        df["Gross Profit"] / df["Sales"].replace(0, pd.NA)
    ) * 100

    return df


df = load_data()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    '<div class="main-title">🍫 Nassau Candy Profitability Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive business intelligence dashboard for profitability, '
    'product performance, and margin analysis.'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("🔎 Dashboard Filters")

# Division
divisions = ["All"] + sorted(df["Division"].dropna().unique().tolist())
selected_division = st.sidebar.selectbox(
    "Division",
    divisions
)

# Region
regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox(
    "Region",
    regions
)

# Date filter
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Product search
product_search = st.sidebar.text_input(
    "Search Product",
    placeholder="Type product name..."
)

# Margin threshold
margin_threshold = st.sidebar.slider(
    "Minimum Profit Margin (%)",
    min_value=0,
    max_value=100,
    value=0,
    step=5
)


# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------
filtered_df = df.copy()

if selected_division != "All":
    filtered_df = filtered_df[
        filtered_df["Division"] == selected_division
    ]

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date)
        & (filtered_df["Order Date"].dt.date <= end_date)
    ]

if product_search:
    filtered_df = filtered_df[
        filtered_df["Product Name"]
        .str.contains(product_search, case=False, na=False)
    ]

filtered_df = filtered_df[
    filtered_df["Profit Margin %"].fillna(0) >= margin_threshold
]


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
total_cost = filtered_df["Cost"].sum()
total_units = filtered_df["Units"].sum()

overall_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

unique_products = filtered_df["Product Name"].nunique()


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">📊 Key Performance Indicators</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Sales</div>
            <div class="kpi-value">${total_sales:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Gross Profit</div>
            <div class="kpi-value">${total_profit:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Profit Margin</div>
            <div class="kpi-value">{overall_margin:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Units Sold</div>
            <div class="kpi-value">{total_units:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Products</div>
            <div class="kpi-value">{unique_products:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ---------------------------------------------------------
# OVERVIEW CHARTS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">📈 Business Performance Overview</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# Division performance
division_summary = (
    filtered_df.groupby("Division", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Units=("Units", "sum")
    )
)

division_summary["Profit Margin %"] = (
    division_summary["Gross_Profit"]
    / division_summary["Sales"]
    * 100
)

with col1:
    fig_division = px.bar(
        division_summary.sort_values("Sales", ascending=False),
        x="Division",
        y="Sales",
        title="Sales by Division",
        text_auto=".2s"
    )

    fig_division.update_layout(
        xaxis_title="Division",
        yaxis_title="Sales ($)",
        height=400
    )

    st.plotly_chart(
        fig_division,
        use_container_width=True
    )

with col2:
    fig_profit = px.bar(
        division_summary.sort_values("Gross_Profit", ascending=False),
        x="Division",
        y="Gross_Profit",
        title="Gross Profit by Division",
        text_auto=".2s"
    )

    fig_profit.update_layout(
        xaxis_title="Division",
        yaxis_title="Gross Profit ($)",
        height=400
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


# ---------------------------------------------------------
# PRODUCT PROFITABILITY
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">🏆 Product Profitability Analysis</div>',
    unsafe_allow_html=True
)

product_summary = (
    filtered_df.groupby("Product Name", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Cost=("Cost", "sum"),
        Units=("Units", "sum")
    )
)

product_summary["Profit Margin %"] = (
    product_summary["Gross_Profit"]
    / product_summary["Sales"]
    * 100
)

top_products = product_summary.sort_values(
    "Gross_Profit",
    ascending=False
).head(10)

fig_products = px.bar(
    top_products.sort_values("Gross_Profit"),
    x="Gross_Profit",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Gross Profit",
    text_auto=".2s"
)

fig_products.update_layout(
    xaxis_title="Gross Profit ($)",
    yaxis_title="Product",
    height=500
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)


# ---------------------------------------------------------
# PRODUCT TABLE
# ---------------------------------------------------------
st.markdown("### Product Profitability Details")

display_products = product_summary.sort_values(
    "Gross_Profit",
    ascending=False
).copy()

display_products["Sales"] = display_products["Sales"].round(2)
display_products["Cost"] = display_products["Cost"].round(2)
display_products["Gross_Profit"] = display_products["Gross_Profit"].round(2)
display_products["Profit Margin %"] = display_products["Profit Margin %"].round(2)

st.dataframe(
    display_products,
    use_container_width=True,
    height=400
)


# ---------------------------------------------------------
# MARGIN RISK ANALYSIS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">⚠️ Margin Risk Analysis</div>',
    unsafe_allow_html=True
)

risk_df = product_summary.sort_values(
    "Profit Margin %",
    ascending=True
).head(10)

fig_risk = px.bar(
    risk_df.sort_values("Profit Margin %"),
    x="Profit Margin %",
    y="Product Name",
    orientation="h",
    title="10 Products with the Lowest Profit Margins",
    text="Profit Margin %"
)

fig_risk.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_risk.update_layout(
    xaxis_title="Profit Margin (%)",
    yaxis_title="Product",
    height=500
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# ---------------------------------------------------------
# PARETO ANALYSIS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">📌 Profit Concentration Analysis</div>',
    unsafe_allow_html=True
)

pareto = product_summary.sort_values(
    "Gross_Profit",
    ascending=False
).copy()

pareto["Cumulative Profit %"] = (
    pareto["Gross_Profit"].cumsum()
    / pareto["Gross_Profit"].sum()
    * 100
)

pareto["Product Rank"] = range(1, len(pareto) + 1)

fig_pareto = px.line(
    pareto,
    x="Product Rank",
    y="Cumulative Profit %",
    title="Cumulative Profit Contribution by Product",
    markers=False
)

fig_pareto.add_hline(
    y=80,
    line_dash="dash",
    annotation_text="80% Profit Level"
)

fig_pareto.update_layout(
    xaxis_title="Product Rank",
    yaxis_title="Cumulative Profit (%)",
    height=450
)

st.plotly_chart(
    fig_pareto,
    use_container_width=True
)


# ---------------------------------------------------------
# BUSINESS INSIGHTS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">💡 Key Business Insights</div>',
    unsafe_allow_html=True
)

if not product_summary.empty:

    highest_profit_product = product_summary.loc[
        product_summary["Gross_Profit"].idxmax()
    ]

    lowest_margin_product = product_summary.loc[
        product_summary["Profit Margin %"].idxmin()
    ]

    best_division = division_summary.loc[
        division_summary["Gross_Profit"].idxmax()
    ]

    insight1 = (
        f"**Top profit-generating division:** "
        f"{best_division['Division']} generated "
        f"${best_division['Gross_Profit']:,.2f} in gross profit."
    )

    insight2 = (
        f"**Highest-profit product:** "
        f"{highest_profit_product['Product Name']} generated "
        f"${highest_profit_product['Gross_Profit']:,.2f} in gross profit."
    )

    insight3 = (
        f"**Lowest-margin product:** "
        f"{lowest_margin_product['Product Name']} has a profit margin "
        f"of {lowest_margin_product['Profit Margin %']:.1f}%."
    )

    st.markdown(
        f'<div class="insight-box">💰 {insight1}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="insight-box">🏆 {insight2}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="insight-box">⚠️ {insight3}</div>',
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# DATA QUALITY CHECK
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">🔍 Data Quality Check</div>',
    unsafe_allow_html=True
)

missing_values = filtered_df.isnull().sum()
missing_values = missing_values[missing_values > 0]

dq1, dq2, dq3 = st.columns(3)

with dq1:
    st.metric(
        "Total Records",
        f"{len(filtered_df):,}"
    )

with dq2:
    st.metric(
        "Total Columns",
        f"{filtered_df.shape[1]}"
    )

with dq3:
    st.metric(
        "Missing-Value Fields",
        f"{len(missing_values)}"
    )

if len(missing_values) > 0:
    st.write("Fields containing missing values:")
    st.dataframe(
        missing_values.rename("Missing Values"),
        use_container_width=True
    )
else:
    st.success("No missing values detected in the filtered dataset.")


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()

st.caption(
    "Nassau Candy Profitability Analysis | "
    "Business Analyst Project | Built with Python, Pandas, Plotly & Streamlit"
)
