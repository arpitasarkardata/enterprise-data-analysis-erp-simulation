"""
GTM Business Intelligence Platform — Streamlit Dashboard
=========================================================
Run with:  streamlit run streamlit_app.py

Requires:
    pip install streamlit anthropic pandas matplotlib mysql-connector-python
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import anthropic
import os

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="GTM BI Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dark theme CSS ────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; color: #c9d1d9; }
    .stMetric { background: #1a1d27; border-radius: 10px; padding: 12px; border: 1px solid #3a3d4d; }
    .stMetricLabel { color: #8b949e !important; font-size: 13px !important; }
    .stMetricValue { color: #7c6af7 !important; font-size: 28px !important; font-weight: 700 !important; }
    .stMetricDelta { font-size: 13px !important; }
    .insight-box {
        background: #161b22; border: 1px solid #7c6af7;
        border-radius: 10px; padding: 16px; margin: 12px 0;
        font-size: 14px; line-height: 1.7; color: #c9d1d9;
    }
    .kpi-header { color: #7c6af7; font-size: 11px; font-weight: 600;
                  letter-spacing: 1.5px; text-transform: uppercase; }
    .sql-box {
        background: #0d1117; border: 1px solid #30363d;
        border-radius: 8px; padding: 12px; font-family: monospace;
        font-size: 13px; color: #22d3ee;
    }
    div[data-testid="stSidebar"] { background-color: #161b22; }
    h1, h2, h3 { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

ACCENT  = '#7c6af7'
ACCENT2 = '#22d3ee'
POSITIVE = '#4ade80'
NEGATIVE = '#f87171'

plt.rcParams.update({
    'figure.facecolor': '#0f1117', 'axes.facecolor': '#1a1d27',
    'axes.edgecolor': '#3a3d4d', 'axes.labelcolor': '#8b949e',
    'xtick.color': '#8b949e', 'ytick.color': '#8b949e',
    'text.color': '#c9d1d9', 'grid.color': '#21262d',
    'grid.linestyle': '--', 'grid.alpha': 0.4,
    'axes.spines.top': False, 'axes.spines.right': False,
})


# ── Data loading (CSV fallback so app works without MySQL) ────
@st.cache_data
def load_data():
    """
    Load from MySQL if available, else generate realistic demo data.
    Replace try block with your actual DB queries once connected.
    """
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=st.secrets.get("DB_HOST", "localhost"),
            user=st.secrets.get("DB_USER", "root"),
            password=st.secrets.get("DB_PASSWORD", ""),
            database="ecommerce"
        )

        df_rev = pd.read_sql("""
            SELECT DATE_FORMAT(o.order_purchase_timestamp,'%Y-%m') AS month,
                   ROUND(SUM(oi.price+oi.freight_value),2) AS total_revenue,
                   COUNT(DISTINCT o.order_id) AS total_orders
            FROM orders o JOIN order_items oi ON o.order_id=oi.order_id
            WHERE o.order_status='delivered'
              AND o.order_purchase_timestamp BETWEEN '2017-01-01' AND '2018-12-31'
            GROUP BY month ORDER BY month
        """, conn)

        df_cat = pd.read_sql("""
            SELECT COALESCE(p.product_category_name,'Unknown') AS category,
                   ROUND(SUM(oi.price+oi.freight_value),2) AS revenue
            FROM order_items oi JOIN products p ON oi.product_id=p.product_id
            JOIN orders o ON oi.order_id=o.order_id
            WHERE o.order_status='delivered'
            GROUP BY category ORDER BY revenue DESC LIMIT 10
        """, conn)

        df_reg = pd.read_sql("""
            SELECT c.customer_state AS state,
                   ROUND(SUM(oi.price+oi.freight_value),2) AS total_revenue,
                   COUNT(DISTINCT c.customer_unique_id) AS unique_customers
            FROM orders o JOIN customers c ON o.customer_id=c.customer_id
            JOIN order_items oi ON o.order_id=oi.order_id
            WHERE o.order_status='delivered'
            GROUP BY state ORDER BY total_revenue DESC LIMIT 10
        """, conn)

        ret = pd.read_sql("""
            WITH f AS (SELECT customer_unique_id, MIN(order_purchase_timestamp) fp
                       FROM orders o JOIN customers c ON o.customer_id=c.customer_id
                       WHERE order_status='delivered' GROUP BY customer_unique_id),
            r AS (SELECT f.customer_unique_id FROM f
                  JOIN orders o ON o.customer_id IN
                      (SELECT customer_id FROM customers WHERE customer_unique_id=f.customer_unique_id)
                  WHERE o.order_purchase_timestamp>f.fp AND o.order_status='delivered'
                  GROUP BY f.customer_unique_id)
            SELECT COUNT(DISTINCT f.customer_unique_id) total_customers,
                   COUNT(DISTINCT r.customer_unique_id) returning_customers
            FROM f LEFT JOIN r ON f.customer_unique_id=r.customer_unique_id
        """, conn)
        conn.close()

        retention_rate = ret['returning_customers'].iloc[0] / ret['total_customers'].iloc[0] * 100
        return df_rev, df_cat, df_reg, retention_rate, "live"

    except Exception:
        # ── Demo data fallback ────────────────────────────────
        months = pd.date_range('2017-01', '2018-12', freq='MS').strftime('%Y-%m').tolist()
        np.random.seed(42)
        base = np.linspace(400000, 1200000, len(months))
        noise = np.random.normal(0, 60000, len(months))
        revenues = (base + noise).clip(200000)

        df_rev = pd.DataFrame({
            'month': months,
            'total_revenue': revenues.round(2),
            'total_orders': (revenues / 150).astype(int)
        })

        categories = ['bed_bath_table','health_beauty','computers_accessories',
                      'sports_leisure','furniture_decor','housewares',
                      'watches_gifts','telephony','auto','toys']
        rev_vals = np.array([1.8,1.6,1.5,1.3,1.1,1.0,0.9,0.85,0.8,0.75]) * 1e6
        df_cat = pd.DataFrame({'category': categories, 'revenue': rev_vals})

        states = ['SP','RJ','MG','RS','PR','SC','BA','GO','ES','PE']
        reg_vals = np.array([5.5,2.1,1.8,0.9,0.85,0.7,0.55,0.4,0.35,0.3]) * 1e6
        df_reg = pd.DataFrame({
            'state': states,
            'total_revenue': reg_vals,
            'unique_customers': (reg_vals / 80).astype(int)
        })

        return df_rev, df_cat, df_reg, 3.2, "demo"


# ── Claude API helper ─────────────────────────────────────────
def ask_claude(prompt, system=None):
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key or api_key == "your_api_key_here":
        return "⚠️ Set ANTHROPIC_API_KEY environment variable to enable AI insights."
    client = anthropic.Anthropic(api_key=api_key)
    kwargs = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}]
    }
    if system:
        kwargs["system"] = system
    resp = client.messages.create(**kwargs)
    return resp.content[0].text


# ── Load data ─────────────────────────────────────────────────
df_rev, df_cat, df_reg, retention_rate, data_mode = load_data()
df_rev['mom_growth'] = df_rev['total_revenue'].pct_change() * 100
rev_2017 = df_rev[df_rev['month'].str.startswith('2017')]['total_revenue'].sum()
rev_2018 = df_rev[df_rev['month'].str.startswith('2018')]['total_revenue'].sum()
yoy = (rev_2018 - rev_2017) / rev_2017 * 100
df_cat['revenue_share'] = (df_cat['revenue'] / df_cat['revenue'].sum() * 100).round(1)


# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🚀 GTM BI Platform")
    st.markdown("**AI-Powered Go-To-Market Analytics**")
    st.divider()

    module = st.radio("📊 Select GTM Module", [
        "🏠 Executive Overview",
        "💰 Revenue Analytics",
        "👥 Customer Retention",
        "🌍 Regional Performance",
        "💬 Natural Language Query",
    ])

    st.divider()
    st.markdown(f"**Data Mode:** {'🟢 Live MySQL' if data_mode=='live' else '🟡 Demo Data'}")
    st.markdown("**Dataset:** Brazilian E-Commerce")
    st.markdown("**Records:** 100,000+ orders")
    st.markdown("**AI Engine:** Claude (Anthropic)")
    st.divider()
    st.caption("Built by Arpita Sarkar · github.com/arpitasarkardata")


# ══════════════════════════════════════════════════════════════
#  PAGE: Executive Overview
# ══════════════════════════════════════════════════════════════
if "Executive Overview" in module:
    st.title("🚀 GTM BI Executive Dashboard")
    st.markdown("*AI-powered insights for Go-To-Market leadership*")
    st.divider()

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("YoY Revenue Growth", f"{yoy:+.1f}%",
                  delta=f"{yoy-15:.1f}% vs target",
                  delta_color="normal")
    with col2:
        avg_mom = df_rev['mom_growth'].mean()
        st.metric("Avg MoM Growth", f"{avg_mom:+.1f}%")
    with col3:
        st.metric("Customer Retention", f"{retention_rate:.1f}%",
                  delta=f"{retention_rate-5:.1f}% vs benchmark",
                  delta_color="inverse")
    with col4:
        st.metric("Top Market", df_reg.iloc[0]['state'],
                  delta=f"{df_reg.iloc[0]['total_revenue']/df_reg['total_revenue'].sum()*100:.0f}% revenue share")

    st.divider()

    # Revenue chart
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df_rev['month'], df_rev['total_revenue']/1e6, color=ACCENT, lw=2.5, marker='o', ms=3)
    ax.fill_between(df_rev['month'], df_rev['total_revenue']/1e6, alpha=0.12, color=ACCENT)
    ax.set_title("Monthly Revenue Trend", color='white', fontsize=13)
    ax.set_ylabel("Revenue (R$ M)", color='#8b949e')
    ax.tick_params(axis='x', rotation=45, labelsize=7)
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    st.markdown("### 🤖 AI Executive Briefing")

    if st.button("Generate AI Insight", type="primary"):
        with st.spinner("Claude is analysing GTM data..."):
            summary = f"""
Revenue YoY growth: {yoy:.1f}%
Customer retention rate: {retention_rate:.2f}%
Top category: {df_cat.iloc[0]['category']} ({df_cat.iloc[0]['revenue_share']}%)
Top region: {df_reg.iloc[0]['state']}
"""
            prompt = f"""You are a Senior GTM BI Analyst.
Based on this data, give a 3-bullet executive briefing (with emojis) + 1 risk + 1 action.
Under 150 words.
{summary}"""
            insight = ask_claude(prompt)
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: Revenue Analytics
# ══════════════════════════════════════════════════════════════
elif "Revenue Analytics" in module:
    st.title("💰 Revenue Analytics")
    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7),
                                        gridspec_kw={'height_ratios': [3, 1]})
        ax1.plot(df_rev['month'], df_rev['total_revenue']/1e6, color=ACCENT, lw=2.5, marker='o', ms=4)
        ax1.fill_between(df_rev['month'], df_rev['total_revenue']/1e6, alpha=0.12, color=ACCENT)
        ax1.set_title("Monthly Revenue + MoM Growth Rate", color='white')
        ax1.set_ylabel("Revenue (R$ M)", color='#8b949e')
        ax1.tick_params(axis='x', rotation=45, labelsize=7)
        ax1.grid(True, alpha=0.2)

        colors = [POSITIVE if v >= 0 else NEGATIVE for v in df_rev['mom_growth'].fillna(0)]
        ax2.bar(df_rev['month'], df_rev['mom_growth'].fillna(0), color=colors, alpha=0.85)
        ax2.axhline(0, color='white', lw=0.8, alpha=0.4)
        ax2.set_ylabel("MoM %", color='#8b949e')
        ax2.tick_params(axis='x', rotation=45, labelsize=7)
        ax2.grid(True, alpha=0.2)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.markdown("#### 📌 Revenue KPIs")
        st.metric("2017 Revenue", f"R$ {rev_2017/1e6:.1f}M")
        st.metric("2018 Revenue", f"R$ {rev_2018/1e6:.1f}M")
        st.metric("YoY Growth", f"{yoy:+.1f}%")
        st.metric("Peak Month", df_rev.loc[df_rev['total_revenue'].idxmax(), 'month'])

    st.divider()
    st.markdown("#### 🏆 Top 10 Categories by Revenue")
    fig2, ax = plt.subplots(figsize=(12, 5))
    bars = ax.barh(df_cat['category'][::-1], df_cat['revenue'][::-1]/1e6, color=ACCENT, alpha=0.85)
    for bar, share in zip(bars, df_cat['revenue_share'][::-1]):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                f'{share}%', va='center', color='#8b949e', fontsize=9)
    ax.set_xlabel("Revenue (R$ M)", color='#8b949e')
    ax.grid(True, axis='x', alpha=0.2)
    plt.tight_layout()
    st.pyplot(fig2)

    if st.button("🤖 AI Revenue Insight"):
        with st.spinner("Generating..."):
            insight = ask_claude(f"""GTM BI briefing for VP Sales.
Revenue YoY: {yoy:.1f}%, top category: {df_cat.iloc[0]['category']} at {df_cat.iloc[0]['revenue_share']}%.
Give 3 bullet insights + 1 action. Under 120 words.""")
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: Customer Retention
# ══════════════════════════════════════════════════════════════
elif "Customer Retention" in module:
    st.title("👥 Customer Retention Analytics")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Retention Rate", f"{retention_rate:.1f}%",
                  delta="⚠️ Below 10% benchmark", delta_color="inverse")
    with col2:
        st.metric("Churn Rate", f"{100-retention_rate:.1f}%")
    with col3:
        st.metric("Top Customer State", df_reg.iloc[0]['state'],
                  delta=f"{df_reg.iloc[0]['unique_customers']:,} customers")

    st.divider()

    # Retention gauge
    fig, ax = plt.subplots(figsize=(6, 4))
    sizes = [retention_rate, 100 - retention_rate]
    colors_pie = [POSITIVE, '#21262d']
    wedges, texts, autotexts = ax.pie(
        sizes, colors=colors_pie, startangle=90,
        autopct='%1.1f%%', pctdistance=0.7,
        wedgeprops={'width': 0.5, 'edgecolor': '#0f1117', 'linewidth': 2}
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(12)
    ax.set_title("Customer Retention vs Churn", color='white', fontsize=13)
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.pyplot(fig)
    with col_b:
        st.markdown("#### 🚨 Retention Alert")
        st.warning(f"""
**Retention rate: {retention_rate:.1f}%**

Industry benchmark for e-commerce: ~20-30%

This signals a **high one-time buyer concentration** — the majority of customers do not return after their first purchase.

**GTM Implication:** Customer acquisition cost is not being recovered through LTV. Urgent need for re-engagement and loyalty strategy.
""")

    if st.button("🤖 AI Retention Insight"):
        with st.spinner("Generating..."):
            insight = ask_claude(f"""Customer Success VP briefing.
Retention rate: {retention_rate:.1f}%, churn: {100-retention_rate:.1f}%.
Top state: {df_reg.iloc[0]['state']}.
Give diagnosis + 2 root causes + 2 GTM interventions. Under 130 words.""")
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: Regional Performance
# ══════════════════════════════════════════════════════════════
elif "Regional Performance" in module:
    st.title("🌍 Regional GTM Performance")
    st.divider()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Revenue by state
    ax1.barh(df_reg['state'][::-1], df_reg['total_revenue'][::-1]/1e6, color=ACCENT, alpha=0.85)
    ax1.set_title("Revenue by State (R$ M)", color='white')
    ax1.set_xlabel("Revenue (R$ M)", color='#8b949e')
    ax1.grid(True, axis='x', alpha=0.2)

    # Customer concentration
    ax2.barh(df_reg['state'][::-1], df_reg['unique_customers'][::-1]/1000, color=ACCENT2, alpha=0.85)
    ax2.set_title("Unique Customers by State (K)", color='white')
    ax2.set_xlabel("Customers (thousands)", color='#8b949e')
    ax2.grid(True, axis='x', alpha=0.2)

    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    st.markdown("#### 📊 Regional Data Table")
    df_display = df_reg.copy()
    df_display['revenue_share'] = (df_display['total_revenue'] / df_display['total_revenue'].sum() * 100).round(1)
    df_display['total_revenue'] = df_display['total_revenue'].apply(lambda x: f"R$ {x/1e6:.2f}M")
    st.dataframe(df_display, use_container_width=True)

    if st.button("🤖 AI Regional Insight"):
        with st.spinner("Generating..."):
            top3 = df_reg.head(3)[['state','total_revenue']].to_string(index=False)
            insight = ask_claude(f"""GTM regional analysis for Sales Ops.
Top states: {top3}
State concentration concern: top state holds {df_reg.iloc[0]['total_revenue']/df_reg['total_revenue'].sum()*100:.0f}% of revenue.
Give 2 insights + 1 expansion recommendation. Under 100 words.""")
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: Natural Language Query
# ══════════════════════════════════════════════════════════════
elif "Natural Language Query" in module:
    st.title("💬 Natural Language → SQL")
    st.markdown("*Ask any business question in plain English — AI converts it to SQL and runs it*")
    st.divider()

    DB_SCHEMA = """
Database: ecommerce (Brazilian E-Commerce, 100K+ orders)
Tables:
- orders(order_id, customer_id, order_status, order_purchase_timestamp)
- customers(customer_id, customer_unique_id, customer_city, customer_state)
- order_items(order_id, product_id, seller_id, price, freight_value)
- products(product_id, product_category_name)
- sellers(seller_id, seller_city, seller_state)
- payments(order_id, payment_type, payment_installments, payment_value)
Joins: orders→customers on customer_id | orders→order_items on order_id
       order_items→products on product_id | order_items→sellers on seller_id
Revenue = price + freight_value. Use order_status='delivered' for revenue queries.
"""

    # Example queries
    st.markdown("#### 💡 Example Questions")
    examples = [
        "Show me total revenue by customer state, top 5",
        "What are the monthly order counts for 2018?",
        "Who are the top 5 sellers by total revenue?",
        "What percentage of orders use credit card?",
        "Show average order value by product category, top 10",
    ]
    selected = st.selectbox("Or pick an example:", ["Type your own..."] + examples)

    user_question = st.text_input(
        "Your question:",
        value="" if selected == "Type your own..." else selected,
        placeholder="e.g. Show me top 5 states by customer count"
    )

    if st.button("🔍 Run Query", type="primary") and user_question:
        system_prompt = f"""You are a SQL expert. Convert the user question to a valid MySQL query.
Schema: {DB_SCHEMA}
Rules: Return ONLY the SQL, no explanation, no backticks, no markdown. Add LIMIT 20."""

        with st.spinner("Claude is generating SQL..."):
            sql = ask_claude(user_question, system=system_prompt).strip()

        st.markdown("#### 🔧 Generated SQL")
        st.markdown(f'<div class="sql-box">{sql}</div>', unsafe_allow_html=True)

        st.markdown("#### 📊 Results")
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password=os.environ.get("DB_PASSWORD", ""),
                database="ecommerce"
            )
            result = pd.read_sql(sql, conn)
            conn.close()
            st.dataframe(result, use_container_width=True)
            st.caption(f"{len(result)} rows returned")
        except Exception as e:
            st.info(f"MySQL not connected — SQL generated successfully. Connect DB to see live results.\n\nError: {e}")

    st.divider()
    st.markdown("""
    #### ℹ️ How it works
    1. You type a question in plain English
    2. Claude (LLM) interprets the business intent and generates MySQL
    3. The query runs against the 100K+ order database
    4. Results display instantly — no SQL knowledge needed

    *This is the same principle behind ThoughtSpot's SearchIQ and conversational BI tools.*
    """)
