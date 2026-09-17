# ==========================================
# E-Commerce Sales Analysis Dashboard
# Submitted By: Anjali Kumari
# Course: BCA 3rd Year
# College: PGGC Sector 11, Chandigarh
# University: Panjab University
# ==========================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------
# Page Configuration
# -----------------------------------------
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)



# -----------------------------------------
# Custom CSS
# -----------------------------------------
st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

h1,h2,h3{
    color:#0b5ed7;
}

div[data-testid="metric-container"]{
    background:white;
    padding:18px;
    border-radius:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,.15);
}

section[data-testid="stSidebar"]{
    background:#123456;
}

/* Sidebar Background */
section[data-testid="stSidebar"]{
    background:#123456;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p{
    color:white !important;
}

/* Text Input */
.stTextInput input{
    background:white !important;
    color:black !important;
    caret-color:black !important;
}

/* Placeholder */
.stTextInput input::placeholder{
    color:gray !important;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"]>div{
    background:white !important;
    color:black !important;
}

/* Dropdown Options */
div[role="listbox"]{
    background:white !important;
    color:black !important;
}

div[role="option"]{
    color:black !important;
}

/* Number Input */
.stNumberInput input{
    color:black !important;
}

/* Text Area */
.stTextArea textarea{
    color:black !important;
}

.stButton>button{
    background:#0b5ed7;
    color:white;
    border-radius:10px;
    height:45px;
    width:100%;
    border:none;
}

.stButton>button:hover{
    background:#084298;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# Header
# -----------------------------------------

st.title("🛒 E-Commerce Sales Analysis Dashboard")

st.markdown("""
### 📚 Data Analytics Project

**Developed By:** Anjali Kumari

**Course:** BCA 3rd Year

**College:** Post Graduate Government College (Coed), Sector 11, Chandigarh

**University:** Panjab University, Chandigarh

**Academic Session:** 2026–27
""")

st.markdown("---")

# -----------------------------------------
# Load Dataset
# -----------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("ecommerce_sales_1000_records.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    return df


df = load_data()

# -----------------------------------------
# Sidebar
# -----------------------------------------

st.sidebar.title("🛒 Dashboard Menu")

st.sidebar.markdown("---")

st.sidebar.header("🔎 Search")

customer = st.sidebar.text_input("Customer Name")

product = st.sidebar.text_input("Product Name")

st.sidebar.markdown("---")

st.sidebar.header("📦 Filters")

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["Category"].unique())
)

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df["Region"].unique())
)

sales_range = st.sidebar.slider(
    "Sales Range",
    int(df["Sales"].min()),
    int(df["Sales"].max()),
    (
        int(df["Sales"].min()),
        int(df["Sales"].max())
    )
)

st.sidebar.markdown("---")

st.sidebar.info("""
### About Project

✔ Python

✔ Pandas

✔ Matplotlib

✔ Streamlit

✔ Data Analytics

Developed by

**Anjali Kumari**
""")

# -----------------------------------------
# Apply Filters
# -----------------------------------------

filtered_df = df.copy()

if customer:

    filtered_df = filtered_df[
        filtered_df["Customer Name"].str.contains(
            customer,
            case=False,
            na=False
        )
    ]

if product:

    filtered_df = filtered_df[
        filtered_df["Product"].str.contains(
            product,
            case=False,
            na=False
        )
    ]

if category != "All":

    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]

if region != "All":

    filtered_df = filtered_df[
        filtered_df["Region"] == region
    ]

filtered_df = filtered_df[
    (filtered_df["Sales"] >= sales_range[0]) &
    (filtered_df["Sales"] <= sales_range[1])
]

# -----------------------------------------
# KPI Cards
# -----------------------------------------

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = len(filtered_df)

avg_sales = filtered_df["Sales"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Total Sales",
    f"₹{total_sales:,.2f}"
)

c2.metric(
    "📈 Total Profit",
    f"₹{total_profit:,.2f}"
)

c3.metric(
    "🛒 Orders",
    total_orders
)

c4.metric(
    "📊 Average Sales",
    f"₹{avg_sales:,.2f}"
)

st.markdown("---")
# ======================================================
# DATA PREVIEW
# ======================================================

st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

st.markdown("---")

# ======================================================
# CATEGORY-WISE SALES
# ======================================================

st.subheader("📊 Category-wise Sales")

category_sales = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(8,5))

bars = ax1.bar(
    category_sales.index,
    category_sales.values
)

ax1.set_title("Category-wise Sales")
ax1.set_xlabel("Category")
ax1.set_ylabel("Sales")

for bar in bars:
    height = bar.get_height()
    ax1.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{height:,.0f}",
        ha="center",
        va="bottom",
        fontsize=8
    )

plt.xticks(rotation=20)

st.pyplot(fig1)

st.markdown("---")

# ======================================================
# REGION-WISE SALES
# ======================================================

st.subheader("🌍 Region-wise Sales")

region_sales = (
    filtered_df
    .groupby("Region")["Sales"]
    .sum()
)

fig2, ax2 = plt.subplots(figsize=(7,7))

ax2.pie(
    region_sales,
    labels=region_sales.index,
    autopct="%1.1f%%",
    startangle=90
)

ax2.set_title("Region-wise Sales")

st.pyplot(fig2)

st.markdown("---")

# ======================================================
# MONTHLY SALES
# ======================================================

st.subheader("📈 Monthly Sales Trend")

filtered_df = filtered_df.copy()

filtered_df["Month"] = filtered_df["Order Date"].dt.month_name()

month_order = [
    "January","February","March","April",
    "May","June","July","August",
    "September","October","November","December"
]

filtered_df["Month"] = pd.Categorical(
    filtered_df["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = (
    filtered_df
    .groupby("Month", observed=False)["Sales"]
    .sum()
)

fig3, ax3 = plt.subplots(figsize=(10,5))

ax3.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o",
    linewidth=3
)

ax3.set_title("Monthly Sales")
ax3.set_xlabel("Month")
ax3.set_ylabel("Sales")

plt.xticks(rotation=45)

st.pyplot(fig3)

st.markdown("---")

# ======================================================
# HISTOGRAM
# ======================================================

st.subheader("📉 Sales Distribution")

fig4, ax4 = plt.subplots(figsize=(8,5))

ax4.hist(
    filtered_df["Sales"],
    bins=15,
    edgecolor="black"
)

ax4.set_title("Sales Distribution")
ax4.set_xlabel("Sales")
ax4.set_ylabel("Frequency")

st.pyplot(fig4)

st.markdown("---")

# ======================================================
# SCATTER PLOT
# ======================================================

st.subheader("⚫ Sales vs Profit")

fig5, ax5 = plt.subplots(figsize=(8,5))

ax5.scatter(
    filtered_df["Sales"],
    filtered_df["Profit"],
    alpha=0.7
)

ax5.set_xlabel("Sales")
ax5.set_ylabel("Profit")
ax5.set_title("Sales vs Profit")

st.pyplot(fig5)

st.markdown("---")
# ======================================================
# TOP 10 PRODUCTS
# ======================================================

st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(
    top_products.reset_index(),
    use_container_width=True
)

fig6, ax6 = plt.subplots(figsize=(10,5))

ax6.barh(
    top_products.index,
    top_products.values
)

ax6.set_title("Top 10 Products")
ax6.set_xlabel("Sales")

plt.gca().invert_yaxis()

st.pyplot(fig6)

st.markdown("---")

# ======================================================
# TOP 10 CUSTOMERS
# ======================================================

st.subheader("👥 Top 10 Customers")

top_customers = (
    filtered_df
    .groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(
    top_customers.reset_index(),
    use_container_width=True
)

fig7, ax7 = plt.subplots(figsize=(10,5))

ax7.barh(
    top_customers.index,
    top_customers.values
)

ax7.set_title("Top Customers")
ax7.set_xlabel("Sales")

plt.gca().invert_yaxis()

st.pyplot(fig7)

st.markdown("---")

# ======================================================
# CATEGORY SUMMARY
# ======================================================

st.subheader("📦 Category Summary")

category_summary = filtered_df.groupby("Category").agg({
    "Sales":"sum",
    "Profit":"sum",
    "Quantity":"sum"
})

st.dataframe(
    category_summary,
    use_container_width=True
)

st.markdown("---")

# ======================================================
# REGION SUMMARY
# ======================================================

st.subheader("🌍 Region Summary")

region_summary = filtered_df.groupby("Region").agg({
    "Sales":"sum",
    "Profit":"sum",
    "Quantity":"sum"
})

st.dataframe(
    region_summary,
    use_container_width=True
)

st.markdown("---")

# ======================================================
# DOWNLOAD CSV
# ======================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered CSV",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)

# ======================================================
# DOWNLOAD EXCEL
# ======================================================

from io import BytesIO

excel_buffer = BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    filtered_df.to_excel(
        writer,
        index=False,
        sheet_name="Sales"
    )

excel_data = excel_buffer.getvalue()

st.download_button(
    label="📥 Download Excel",
    data=excel_data,
    file_name="filtered_sales.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.markdown("---")
# ======================================================
# BUSINESS INSIGHTS
# ======================================================

st.header("🧠 Business Insights")

col1, col2 = st.columns(2)

with col1:
    best_category = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    best_category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .max()
    )

    st.success(
        f"🏆 Best Category: {best_category}\n\n"
        f"Sales: ₹{best_category_sales:,.2f}"
    )

with col2:
    best_region = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    best_region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .max()
    )

    st.success(
        f"🌍 Best Region: {best_region}\n\n"
        f"Sales: ₹{best_region_sales:,.2f}"
    )

st.markdown("---")

# ======================================================
# HIGHEST SELLING PRODUCT
# ======================================================

st.subheader("⭐ Highest Selling Product")

top_product = (
    filtered_df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.info(
    f"""
**Product:** {top_product.index[0]}

**Sales:** ₹{top_product.iloc[0]:,.2f}
"""
)

st.markdown("---")

# ======================================================
# HIGHEST PROFIT PRODUCT
# ======================================================

st.subheader("💰 Highest Profit Product")

profit_product = (
    filtered_df.groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

st.info(
    f"""
**Product:** {profit_product.index[0]}

**Profit:** ₹{profit_product.iloc[0]:,.2f}
"""
)

st.markdown("---")

# ======================================================
# PROJECT SUMMARY
# ======================================================

st.header("📈 Dashboard Summary")

summary = f"""

✔ Total Records : {len(filtered_df)}

✔ Total Sales : ₹{total_sales:,.2f}

✔ Total Profit : ₹{total_profit:,.2f}

✔ Average Sales : ₹{avg_sales:,.2f}

✔ Categories : {filtered_df['Category'].nunique()}

✔ Products : {filtered_df['Product'].nunique()}

✔ Customers : {filtered_df['Customer Name'].nunique()}

✔ Regions : {filtered_df['Region'].nunique()}

"""

st.success(summary)

st.markdown("---")

# ======================================================
# CURRENT DATE & TIME
# ======================================================

from datetime import datetime

now = datetime.now()

st.caption(
    f"🕒 Dashboard Generated on: {now.strftime('%d-%m-%Y %I:%M %p')}"
)

st.markdown("---")

# ======================================================
# FOOTER
# ======================================================

st.markdown("""
---
<center>

## 🎓 E-Commerce Sales Analysis Project

**Developed By**

### Anjali Kumari

**Course:** BCA 3rd Year

**Subject:** Data Analytics

**College:** Post Graduate Government College (Coed), Sector 11, Chandigarh

**University:** Panjab University, Chandigarh

**Academic Session:** 2026–27

Made using ❤️ Python • Pandas • Matplotlib • Streamlit

</center>
""", unsafe_allow_html=True)

st.balloons()