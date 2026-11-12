
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Customer Retention Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PATHS
# ============================================================
APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

RAW_FILE = PROJECT_DIR / "data" / "European_Bank.csv"
PROCESSED_FILE = PROJECT_DIR / "outputs" / "customer_retention_analysis.csv"

# ============================================================
# GLOBAL STYLE
# IMPORTANT:
# Every HTML block below uses unsafe_allow_html=True.
# This prevents HTML tags from appearing as text.
# ============================================================
st.markdown(
    """
    <style>
        /* ---------- Main application ---------- */
        .stApp {
            background:
                radial-gradient(circle at top right, rgba(64, 91, 180, 0.14), transparent 28%),
                linear-gradient(135deg, #07111f 0%, #0a1424 48%, #07101d 100%);
            color: #f5f7fb;
        }

        .main .block-container {
            padding: 2rem 2.5rem 3rem 2.5rem;
            max-width: 1550px;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #091626 0%, #07111f 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        section[data-testid="stSidebar"] .block-container {
            padding: 1.4rem 1rem;
        }

        .brand-box {
            padding: 18px;
            border-radius: 16px;
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 22px;
        }

        .brand-icon {
            font-size: 28px;
            margin-bottom: 8px;
        }

        .brand-name {
            font-size: 20px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 0.2px;
        }

        .brand-caption {
            margin-top: 6px;
            color: #8ea4bd;
            font-size: 11px;
            line-height: 1.5;
            letter-spacing: 0.7px;
            text-transform: uppercase;
        }

        .side-heading {
            color: #ffffff;
            font-size: 14px;
            font-weight: 800;
            margin: 22px 0 8px 0;
        }

        .side-note {
            color: #8ea4bd;
            font-size: 12px;
            line-height: 1.5;
        }

        /* ---------- Hero ---------- */
        .hero {
            padding: 26px 28px;
            border-radius: 22px;
            background:
                linear-gradient(135deg, rgba(24, 39, 73, 0.95), rgba(10, 22, 40, 0.96));
            border: 1px solid rgba(119, 169, 255, 0.18);
            box-shadow: 0 20px 50px rgba(0,0,0,0.18);
            margin-bottom: 22px;
        }

        .hero-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
        }

        .hero-kicker {
            color: #80bfff;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1.8px;
            text-transform: uppercase;
        }

        .hero-title {
            color: #ffffff;
            font-size: 32px;
            font-weight: 850;
            margin-top: 7px;
            line-height: 1.15;
        }

        .hero-subtitle {
            color: #a7b8cb;
            font-size: 14px;
            margin-top: 9px;
            line-height: 1.6;
        }

        .live-pill {
            white-space: nowrap;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(58, 211, 137, 0.10);
            border: 1px solid rgba(58, 211, 137, 0.24);
            color: #76e5aa;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.7px;
        }

        /* ---------- Section headers ---------- */
        .section-header {
            margin: 26px 0 14px 0;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }

        .section-title {
            color: #ffffff;
            font-size: 21px;
            font-weight: 800;
        }

        .section-description {
            color: #8ea4bd;
            font-size: 13px;
            margin-top: 5px;
        }

        /* ---------- KPI cards ---------- */
        .kpi-card {
            min-height: 150px;
            padding: 20px;
            border-radius: 18px;
            background: linear-gradient(145deg, rgba(20, 34, 56, 0.96), rgba(13, 25, 43, 0.96));
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 12px 30px rgba(0,0,0,0.12);
        }

        .kpi-label {
            color: #8ea4bd;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.7px;
        }

        .kpi-value {
            color: #ffffff;
            font-size: 30px;
            font-weight: 850;
            margin-top: 10px;
        }

        .kpi-description {
            color: #71879e;
            font-size: 11px;
            margin-top: 8px;
            line-height: 1.4;
        }

        /* ---------- Info cards ---------- */
        .info-card {
            padding: 18px 20px;
            border-radius: 16px;
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.07);
            margin: 8px 0 18px 0;
        }

        .info-title {
            color: #ffffff;
            font-size: 14px;
            font-weight: 800;
        }

        .info-text {
            color: #91a5bb;
            font-size: 12px;
            margin-top: 5px;
            line-height: 1.5;
        }

        /* ---------- Alert ---------- */
        .alert-box {
            padding: 15px 18px;
            border-radius: 14px;
            background: rgba(255, 176, 71, 0.08);
            border: 1px solid rgba(255, 176, 71, 0.18);
            color: #ffd08a;
            font-size: 13px;
            line-height: 1.5;
            margin: 12px 0;
        }

        /* ---------- Footer ---------- */
        .footer {
            margin-top: 35px;
            padding-top: 18px;
            border-top: 1px solid rgba(255,255,255,0.08);
            color: #647990;
            text-align: center;
            font-size: 11px;
        }

        /* ---------- Streamlit controls ---------- */
        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.07);
            padding: 15px;
            border-radius: 15px;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
        }

        .stDownloadButton button {
            border-radius: 10px;
        }

        /* Make normal Streamlit text readable */
        label, .stMarkdown, .stCaption {
            color: #d9e2ed !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def section_header(title, description=""):
    html = f"""
    <div class="section-header">
        <div class="section-title">{title}</div>
        <div class="section-description">{description}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def kpi_card(label, value, description=""):
    html = f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-description">{description}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def info_card(title, text):
    html = f"""
    <div class="info-card">
        <div class="info-title">{title}</div>
        <div class="info-text">{text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def format_number(value):
    return f"{value:,.0f}"


def format_percent(value):
    return f"{value:.2f}%"


def plot_layout(fig, height=390):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce6f1"),
        margin=dict(l=25, r=20, t=45, b=30),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dce6f1")
        ),
        hoverlabel=dict(
            bgcolor="#172338",
            font_color="#ffffff"
        )
    )
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.07)",
        zerolinecolor="rgba(255,255,255,0.07)"
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.07)",
        zerolinecolor="rgba(255,255,255,0.07)"
    )
    return fig


# ============================================================
# DATA PREPARATION
# ============================================================
@st.cache_data
def load_data():
    """
    Load processed data if available.
    Otherwise load the original CSV and create dashboard columns.
    """

    # Base columns that must exist in the customer-level dataset
    required_columns = [
        "CustomerId", "CreditScore", "Age", "Tenure", "Balance",
        "NumOfProducts", "HasCrCard", "IsActiveMember",
        "EstimatedSalary", "Exited"
    ]

    # Try processed file first, but only use it if it is actually a
    # customer-level dataset. This prevents KeyError when an old/wrong
    # output CSV is present.
    data = None

    if PROCESSED_FILE.exists():
        try:
            processed = pd.read_csv(PROCESSED_FILE)
            processed.columns = [str(c).strip() for c in processed.columns]

            if all(col in processed.columns for col in required_columns):
                data = processed
        except Exception:
            data = None

    # If processed CSV is missing required columns, use the original CSV.
    if data is None and RAW_FILE.exists():
        data = pd.read_csv(RAW_FILE)

    if data is None:
        return None

    # Clean column names
    data.columns = [str(c).strip() for c in data.columns]

    # Remove accidental index columns
    unwanted = [
        col for col in data.columns
        if str(col).lower().startswith("unnamed")
    ]
    if unwanted:
        data = data.drop(columns=unwanted)

    # Check that the raw customer dataset has the required fields.
    missing_required = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing_required:
        raise ValueError(
            "The CSV does not contain the required customer columns: "
            + ", ".join(missing_required)
            + "\n\nExpected columns include: "
            + ", ".join(required_columns)
        )

    # --------------------------------------------------------
    # Required numeric conversions
    # --------------------------------------------------------
    numeric_columns = [
        "CustomerId",
        "CreditScore",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary",
        "Exited"
    ]

    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    # --------------------------------------------------------
    # Engagement Profile
    # --------------------------------------------------------
    if "EngagementProfile" not in data.columns:
        def engagement_profile(row):
            active = row["IsActiveMember"]
            products = row["NumOfProducts"]
            balance = row["Balance"]

            if active == 1 and products >= 2:
                return "Active Multi-Product"
            elif active == 1 and products < 2:
                return "Active Low-Product"
            elif active == 0 and balance > 0:
                return "Inactive High-Balance"
            else:
                return "Inactive Low-Engagement"

        data["EngagementProfile"] = data.apply(
            engagement_profile,
            axis=1
        )

    # --------------------------------------------------------
    # Product Depth
    # --------------------------------------------------------
    if "ProductDepth" not in data.columns:
        data["ProductDepth"] = np.where(
            data["NumOfProducts"] >= 2,
            "Multi Product",
            "Single Product"
        )

    # --------------------------------------------------------
    # Balance Tier
    # --------------------------------------------------------
    if "BalanceTier" not in data.columns:
        try:
            data["BalanceTier"] = pd.qcut(
                data["Balance"],
                q=4,
                labels=["Low", "Medium", "High", "Very High"],
                duplicates="drop"
            )
        except Exception:
            data["BalanceTier"] = "Standard"

    # --------------------------------------------------------
    # High-value customer
    # --------------------------------------------------------
    balance_threshold = data["Balance"].quantile(0.75)
    salary_threshold = data["EstimatedSalary"].quantile(0.75)

    if "HighValueCustomer" not in data.columns:
        data["HighValueCustomer"] = (
            (data["Balance"] >= balance_threshold) |
            (data["EstimatedSalary"] >= salary_threshold)
        )

    # --------------------------------------------------------
    # Disengaged
    # --------------------------------------------------------
    if "Disengaged" not in data.columns:
        data["Disengaged"] = data["IsActiveMember"] == 0

    # --------------------------------------------------------
    # High-value disengaged
    # --------------------------------------------------------
    if "HighValueDisengaged" not in data.columns:
        data["HighValueDisengaged"] = (
            data["HighValueCustomer"] &
            data["Disengaged"]
        )

    # --------------------------------------------------------
    # Balance / Salary ratio
    # --------------------------------------------------------
    if "BalanceSalaryRatio" not in data.columns:
        data["BalanceSalaryRatio"] = (
            data["Balance"] /
            data["EstimatedSalary"].replace(0, np.nan)
        )

    # --------------------------------------------------------
    # Relationship Strength
    # --------------------------------------------------------
    if "RelationshipStrength" not in data.columns:
        max_tenure = max(data["Tenure"].max(), 1)

        data["RelationshipStrength"] = (
            data["IsActiveMember"] * 40
            + (data["NumOfProducts"] >= 2).astype(int) * 30
            + data["HasCrCard"] * 15
            + (data["Tenure"] / max_tenure) * 15
        )

    # --------------------------------------------------------
    # Relationship Tier
    # --------------------------------------------------------
    if "RelationshipTier" not in data.columns:
        data["RelationshipTier"] = pd.cut(
            data["RelationshipStrength"],
            bins=[-1, 25, 50, 75, 101],
            labels=[
                "Weak",
                "Moderate",
                "Strong",
                "Very Strong"
            ]
        )

    # --------------------------------------------------------
    # Retention Segment
    # --------------------------------------------------------
    if "RetentionSegment" not in data.columns:
        data["RetentionSegment"] = pd.cut(
            data["RelationshipStrength"],
            bins=[-1, 25, 50, 75, 101],
            labels=[
                "Critical Risk",
                "Moderate Risk",
                "Stable",
                "Strong"
            ]
        )

    # --------------------------------------------------------
    # Useful display columns
    # --------------------------------------------------------
    if "Activity" not in data.columns:
        data["Activity"] = np.where(
            data["IsActiveMember"] == 1,
            "Active",
            "Inactive"
        )

    if "ChurnStatus" not in data.columns:
        data["ChurnStatus"] = np.where(
            data["Exited"] == 1,
            "Churned",
            "Retained"
        )

    data = data.dropna(
        subset=[
            "CreditScore",
            "Age",
            "Tenure",
            "Balance",
            "NumOfProducts",
            "HasCrCard",
            "IsActiveMember",
            "EstimatedSalary",
            "Exited"
        ]
    ).copy()

    return data


df = load_data()

# ============================================================
# FILE ERROR
# ============================================================
if df is None:
    st.error("Dataset file was not found.")

    st.markdown(
        f"""
        **Required project structure:**

        ```
        Customer_Retention_Analytics/
        ├── data/
        │   └── European_Bank.csv
        ├── outputs/
        │   └── customer_retention_analysis.csv
        └── app/
            └── streamlit_app.py
        ```

        Put your CSV inside the `data` folder with this exact name:

        `European_Bank.csv`
        """,
        unsafe_allow_html=False
    )

    st.stop()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:

    st.markdown(
        """
        <div class="brand-box">
            <div class="brand-icon">🏦</div>
            <div class="brand-name">Retention Intelligence</div>
            <div class="brand-caption">
                Customer engagement analytics
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-heading">Navigation</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Engagement Intelligence",
            "Product Intelligence",
            "Customer Risk",
            "Retention Strength"
        ],
        label_visibility="collapsed"
    )

    st.markdown(
        '<div class="side-heading">Filters</div>',
        unsafe_allow_html=True
    )

    # Geography filter
    if "Geography" in df.columns:
        geographies = sorted(
            df["Geography"].dropna().unique().tolist()
        )
        selected_geo = st.multiselect(
            "Geography",
            geographies,
            default=geographies
        )
    else:
        selected_geo = []

    # Gender filter
    if "Gender" in df.columns:
        genders = sorted(
            df["Gender"].dropna().unique().tolist()
        )
        selected_gender = st.multiselect(
            "Gender",
            genders,
            default=genders
        )
    else:
        selected_gender = []

    # Activity filter
    selected_activity = st.multiselect(
        "Activity",
        ["Active", "Inactive"],
        default=["Active", "Inactive"]
    )

    # Product filter
    product_values = sorted(
        df["NumOfProducts"].dropna().unique().astype(int).tolist()
    )

    selected_products = st.multiselect(
        "Number of Products",
        product_values,
        default=product_values
    )

# ============================================================
# APPLY FILTERS
# ============================================================
filtered = df.copy()

if "Geography" in filtered.columns and selected_geo:
    filtered = filtered[
        filtered["Geography"].isin(selected_geo)
    ]

if "Gender" in filtered.columns and selected_gender:
    filtered = filtered[
        filtered["Gender"].isin(selected_gender)
    ]

if selected_activity:
    filtered = filtered[
        filtered["Activity"].isin(selected_activity)
    ]

if selected_products:
    filtered = filtered[
        filtered["NumOfProducts"].isin(selected_products)
    ]

if filtered.empty:
    st.warning("No customers match the selected filters.")
    st.stop()

# ============================================================
# GLOBAL CALCULATIONS
# ============================================================
total_customers = len(filtered)
churned_customers = int(filtered["Exited"].sum())
retained_customers = total_customers - churned_customers

churn_rate = (
    filtered["Exited"].mean() * 100
    if total_customers > 0 else 0
)

active_rate = (
    filtered["IsActiveMember"].mean() * 100
    if total_customers > 0 else 0
)

high_value_at_risk = int(
    filtered["HighValueDisengaged"].sum()
)

# ============================================================
# HERO
# ============================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-top">
            <div>
                <div class="hero-kicker">Customer Analytics Platform</div>
                <div class="hero-title">
                    Customer Retention Intelligence
                </div>
                <div class="hero-subtitle">
                    Customer engagement, product utilization,
                    relationship strength & churn analytics
                </div>
            </div>
            <div class="live-pill">● LIVE ANALYTICS</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ============================================================
if page == "Executive Overview":

    section_header(
        "Executive Overview",
        "A high-level view of customer retention and engagement."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card(
            "Total Customers",
            format_number(total_customers),
            "Customers in current filter"
        )

    with c2:
        kpi_card(
            "Churn Rate",
            format_percent(churn_rate),
            "Customers who exited"
        )

    with c3:
        kpi_card(
            "Active Rate",
            format_percent(active_rate),
            "Customers currently active"
        )

    with c4:
        kpi_card(
            "High-Value At Risk",
            format_number(high_value_at_risk),
            "High-value disengaged customers"
        )

    section_header(
        "Churn Overview",
        "Understand retained and churned customer distribution."
    )

    col1, col2 = st.columns(2)

    with col1:
        retention_mix = pd.DataFrame({
            "Status": ["Retained", "Churned"],
            "Customers": [
                retained_customers,
                churned_customers
            ]
        })

        fig = px.pie(
            retention_mix,
            names="Status",
            values="Customers",
            hole=0.62,
            title="Customer Retention Mix"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="label+percent"
        )

        st.plotly_chart(
            plot_layout(fig, 410),
            use_container_width=True
        )

    with col2:
        activity_churn = (
            filtered.groupby("Activity", as_index=False)["Exited"]
            .mean()
        )

        activity_churn["ChurnRate"] = (
            activity_churn["Exited"] * 100
        )

        fig = px.bar(
            activity_churn,
            x="Activity",
            y="ChurnRate",
            text="ChurnRate",
            title="Churn Rate by Activity"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        fig.update_yaxes(title="Churn Rate (%)")
        st.plotly_chart(
            plot_layout(fig, 410),
            use_container_width=True
        )

    section_header(
        "Key Customer Signals",
        "Quick indicators for relationship and retention analysis."
    )

    s1, s2, s3 = st.columns(3)

    with s1:
        multi_product_rate = (
            (filtered["NumOfProducts"] >= 2).mean() * 100
        )
        kpi_card(
            "Multi-Product Rate",
            format_percent(multi_product_rate),
            "Customers using 2 or more products"
        )

    with s2:
        avg_balance = filtered["Balance"].mean()
        kpi_card(
            "Average Balance",
            f"€{avg_balance:,.0f}",
            "Average customer balance"
        )

    with s3:
        avg_relationship = filtered[
            "RelationshipStrength"
        ].mean()
        kpi_card(
            "Relationship Strength",
            f"{avg_relationship:.1f}/100",
            "Average relationship score"
        )

# ============================================================
# PAGE 2: ENGAGEMENT INTELLIGENCE
# ============================================================
elif page == "Engagement Intelligence":

    section_header(
        "Engagement Intelligence",
        "Customer distribution and churn across engagement profiles."
    )

    profile_counts = (
        filtered["EngagementProfile"]
        .value_counts()
        .reset_index()
    )

    profile_counts.columns = [
        "Profile",
        "Customers"
    ]

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            profile_counts,
            x="Customers",
            y="Profile",
            orientation="h",
            text="Customers",
            title="Engagement Distribution"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            plot_layout(fig, 430),
            use_container_width=True
        )

    with col2:
        profile_churn = (
            filtered.groupby(
                "EngagementProfile",
                as_index=False
            )["Exited"].mean()
        )

        profile_churn["ChurnRate"] = (
            profile_churn["Exited"] * 100
        )

        fig = px.bar(
            profile_churn,
            x="EngagementProfile",
            y="ChurnRate",
            text="ChurnRate",
            title="Churn Rate by Engagement Profile"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        fig.update_yaxes(title="Churn Rate (%)")
        fig.update_xaxes(tickangle=-25)

        st.plotly_chart(
            plot_layout(fig, 430),
            use_container_width=True
        )

    section_header(
        "Activity & Financial Commitment",
        "Compare customer activity with balances."
    )

    col1, col2 = st.columns(2)

    with col1:
        activity_balance = (
            filtered.groupby("Activity", as_index=False)
            .agg(
                Customers=("CustomerId", "count"),
                AverageBalance=("Balance", "mean")
            )
        )

        fig = px.bar(
            activity_balance,
            x="Activity",
            y="AverageBalance",
            text="AverageBalance",
            title="Average Balance by Activity"
        )

        fig.update_traces(
            texttemplate="€%{text:,.0f}",
            textposition="outside"
        )

        fig.update_yaxes(title="Average Balance (€)")

        st.plotly_chart(
            plot_layout(fig, 410),
            use_container_width=True
        )

    with col2:
        fig = px.scatter(
            filtered,
            x="Balance",
            y="EstimatedSalary",
            color="Activity",
            hover_data=[
                "CustomerId",
                "Age",
                "NumOfProducts",
                "Exited"
            ],
            title="Balance vs Estimated Salary",
            opacity=0.65
        )

        fig.update_xaxes(title="Balance (€)")
        fig.update_yaxes(title="Estimated Salary (€)")

        st.plotly_chart(
            plot_layout(fig, 410),
            use_container_width=True
        )

# ============================================================
# PAGE 3: PRODUCT INTELLIGENCE
# ============================================================
elif page == "Product Intelligence":

    section_header(
        "Product Intelligence",
        "Analyze product depth and its relationship with retention."
    )

    product_summary = (
        filtered.groupby("NumOfProducts", as_index=False)
        .agg(
            Customers=("CustomerId", "count"),
            ChurnRate=("Exited", "mean")
        )
    )

    product_summary["ChurnRate"] *= 100

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            product_summary,
            x="NumOfProducts",
            y="Customers",
            text="Customers",
            title="Customers by Product Count"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_xaxes(
            title="Number of Products",
            dtick=1
        )
        fig.update_yaxes(title="Customers")

        st.plotly_chart(
            plot_layout(fig, 420),
            use_container_width=True
        )

    with col2:
        fig = px.bar(
            product_summary,
            x="NumOfProducts",
            y="ChurnRate",
            text="ChurnRate",
            title="Churn Rate by Product Count"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        fig.update_xaxes(
            title="Number of Products",
            dtick=1
        )
        fig.update_yaxes(title="Churn Rate (%)")

        st.plotly_chart(
            plot_layout(fig, 420),
            use_container_width=True
        )

    section_header(
        "Product Depth",
        "Single-product and multi-product customer comparison."
    )

    depth_summary = (
        filtered.groupby("ProductDepth", as_index=False)
        .agg(
            Customers=("CustomerId", "count"),
            ChurnRate=("Exited", "mean")
        )
    )

    depth_summary["ChurnRate"] *= 100

    st.dataframe(
        depth_summary.style.format({
            "Customers": "{:,.0f}",
            "ChurnRate": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    section_header(
        "Credit Card Stickiness",
        "Customer activity and churn among credit-card holders."
    )

    card_summary = (
        filtered.groupby("HasCrCard", as_index=False)
        .agg(
            Customers=("CustomerId", "count"),
            ChurnRate=("Exited", "mean")
        )
    )

    card_summary["CreditCard"] = np.where(
        card_summary["HasCrCard"] == 1,
        "Has Credit Card",
        "No Credit Card"
    )

    card_summary["ChurnRate"] *= 100

    fig = px.bar(
        card_summary,
        x="CreditCard",
        y="ChurnRate",
        text="ChurnRate",
        title="Churn Rate by Credit Card Ownership"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_yaxes(title="Churn Rate (%)")

    st.plotly_chart(
        plot_layout(fig, 400),
        use_container_width=True
    )

# ============================================================
# PAGE 4: CUSTOMER RISK
# ============================================================
elif page == "Customer Risk":

    section_header(
        "Customer Risk",
        "Identify disengaged and high-value customers requiring attention."
    )

    risk_customers = filtered[
        filtered["HighValueDisengaged"] == True
    ].copy()

    risk_count = len(risk_customers)

    rc1, rc2, rc3 = st.columns(3)

    with rc1:
        kpi_card(
            "High-Value Disengaged",
            format_number(risk_count),
            "Customers with high-value indicators but inactive status"
        )

    with rc2:
        risk_churn = (
            risk_customers["Exited"].mean() * 100
            if risk_count > 0 else 0
        )

        kpi_card(
            "Risk Group Churn",
            format_percent(risk_churn),
            "Churn rate within the risk group"
        )

    with rc3:
        avg_risk_balance = (
            risk_customers["Balance"].mean()
            if risk_count > 0 else 0
        )

        kpi_card(
            "Avg. Risk Balance",
            f"€{avg_risk_balance:,.0f}",
            "Average balance in risk group"
        )

    if risk_count > 0:
        st.markdown(
            """
            <div class="alert-box">
                <strong>Risk signal:</strong>
                These customers combine financial value indicators
                with inactive engagement status.
            </div>
            """,
            unsafe_allow_html=True
        )

    section_header(
        "Risk Customer Table",
        "Filterable customer-level view of high-value disengaged customers."
    )

    display_columns = [
        "CustomerId",
        "Surname",
        "Geography",
        "Gender",
        "Age",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "Exited",
        "RelationshipStrength",
        "RetentionSegment"
    ]

    display_columns = [
        col for col in display_columns
        if col in risk_customers.columns
    ]

    risk_display = risk_customers[display_columns].copy()

    st.dataframe(
        risk_display,
        use_container_width=True,
        hide_index=True
    )

    csv_data = risk_display.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Risk Customers CSV",
        data=csv_data,
        file_name="high_value_disengaged_customers.csv",
        mime="text/csv"
    )

# ============================================================
# PAGE 5: RETENTION STRENGTH
# ============================================================
elif page == "Retention Strength":

    section_header(
        "Retention Strength",
        "Relationship strength based on activity, products, card ownership and tenure."
    )

    tier_summary = (
        filtered.groupby(
            "RelationshipTier",
            observed=False,
            as_index=False
        )
        .agg(
            Customers=("CustomerId", "count"),
            ChurnRate=("Exited", "mean"),
            AverageScore=("RelationshipStrength", "mean")
        )
    )

    tier_summary["ChurnRate"] *= 100

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            tier_summary,
            x="RelationshipTier",
            y="Customers",
            text="Customers",
            title="Customers by Relationship Strength"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            plot_layout(fig, 420),
            use_container_width=True
        )

    with col2:
        fig = px.bar(
            tier_summary,
            x="RelationshipTier",
            y="ChurnRate",
            text="ChurnRate",
            title="Churn Rate by Relationship Strength"
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        fig.update_yaxes(title="Churn Rate (%)")

        st.plotly_chart(
            plot_layout(fig, 420),
            use_container_width=True
        )

    section_header(
        "Relationship Strength Summary",
        "Summary of customer volume, score and churn."
    )

    st.dataframe(
        tier_summary.style.format({
            "Customers": "{:,.0f}",
            "ChurnRate": "{:.2f}%",
            "AverageScore": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    section_header(
        "Relationship Strength Distribution",
        "Distribution of the calculated relationship strength score."
    )

    fig = px.histogram(
        filtered,
        x="RelationshipStrength",
        nbins=25,
        title="Relationship Strength Distribution"
    )

    fig.update_xaxes(
        title="Relationship Strength Score"
    )
    fig.update_yaxes(
        title="Customers"
    )

    st.plotly_chart(
        plot_layout(fig, 400),
        use_container_width=True
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer">
        Customer Retention Intelligence • Customer Engagement & Product Utilization Analytics
    </div>
    """,
    unsafe_allow_html=True
)
