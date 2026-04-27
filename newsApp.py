# ============================================================
#  INDIA PULSE — Simple Streamlit Dashboard
#
#  How to run:
#    1. Run the notebook first → it creates news_data.csv
#    2. Open terminal in the same folder
#    3. Type:  streamlit run app.py
#    4. Browser opens at http://localhost:8501
# ============================================================

import streamlit as st
import pandas as pd

# ── Page setup ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BharatBrief",
    page_icon="ʙʜ",
    layout="wide"
)

# ── Emoji map for sentiment labels ────────────────────────────────────────────
EMOJI = {
    "Positive": "🟢",
    "Negative": "🔴",
    "Neutral":  "🟡"
}

# ── Load data from CSV ────────────────────────────────────────────────────────
# @st.cache_data means Streamlit loads the file once and remembers it
# instead of re-reading the file on every button click
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("news_data.csv")
        df["published_at"] = pd.to_datetime(df["published_at"])  # Convert date column
        return df
    except FileNotFoundError:
        return None   # We'll show an error message below if file is missing

df = load_data()

# # ── Header 
# st.title(" BharatBrief")
# st.caption("Live news headlines with sentiment analysis · Powered by NewsAPI + VADER")
# st.divider()

st.title(" BharatBrief")

st.markdown(
    "<h3 style='color:#6b7280; margin-top:-10px;'> Track the Nation Through Data.</h3>",
    unsafe_allow_html=True
)

st.divider()

# ── Show error if CSV not found 
if df is None:
    st.error(" news_data.csv not found! Please run the Jupyter notebook first.")
    st.code("Step: Run all cells in india_pulse_simple.ipynb → then come back here")
    st.stop()   # Stop rendering the rest of the app

# ── Show total count ──────────────────────────────────────────────────────────
total   = len(df)
pos_pct = round((df["sentiment"] == "Positive").mean() * 100)
neg_pct = round((df["sentiment"] == "Negative").mean() * 100)
neu_pct = 100 - pos_pct - neg_pct

col1, col2, col3, col4 = st.columns(4)
col1.metric(" Total Articles",  total)
col2.metric(" Positive",        f"{pos_pct}%")
col3.metric(" Negative",        f"{neg_pct}%")
col4.metric(" Neutral",         f"{neu_pct}%")

st.divider()

# ── 3 Tabs ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    " Morning Briefing — India",
    " Company News",
    " Tech & AI"
])


# ════════════════════════════════════════════════════════════════════════════
#  TAB 1 — INDIA MORNING BRIEFING
# ════════════════════════════════════════════════════════════════════════════
with tab1:

    st.subheader(" Top India Headlines")
    st.write("Latest news from India, scored by sentiment.")

    # Filter only India category articles
    df_india = df[df["category"] == "india"].copy()

    if df_india.empty:
        st.warning("No India news found. Check your notebook ran correctly.")
    else:
        # Sentiment filter — user can filter by Positive / Negative / Neutral
        sentiment_choice = st.selectbox(
            "Filter by sentiment",
            ["All", "Positive", "Negative", "Neutral"],
            key="india_filter"
        )

        # Apply filter if user chose something specific
        if sentiment_choice != "All":
            df_india = df_india[df_india["sentiment"] == sentiment_choice]

        st.write(f"Showing **{len(df_india)}** articles")
        st.divider()

        # Show each headline as a simple card
        for _, row in df_india.iterrows():
            emoji = EMOJI.get(row["sentiment"], "")
            time  = pd.to_datetime(row["published_at"]).strftime("%d %b, %I:%M %p")

            # Clickable headline title — links to original article
            st.markdown(f"### {emoji} [{row['title']}]({row['url']})")
            st.caption(f" {row['source']}  ·   {time}  ·  Sentiment: **{row['sentiment']}** (score: {row['score']})")
            st.divider()


# ════════════════════════════════════════════════════════════════════════════
#  TAB 2 — COMPANY NEWS
# ════════════════════════════════════════════════════════════════════════════
with tab2:

    st.subheader(" Company News Tracker")
    st.write("News articles mentioning specific Indian companies, scored by sentiment.")

    # Filter only company category articles
    df_comp = df[df["category"] == "company"].copy()

    if df_comp.empty:
        st.warning("No company news found. Check your notebook ran correctly.")
    else:
        # Two side-by-side filters: company selector + sentiment filter
        col_a, col_b = st.columns(2)

        with col_a:
            # Get list of companies available in the data
            companies = ["All Companies"] + sorted(df_comp["company"].dropna().unique().tolist())
            company_choice = st.selectbox("Select Company", companies, key="comp_select")

        with col_b:
            comp_sent = st.selectbox(
                "Filter by Sentiment",
                ["All", "Positive", "Negative", "Neutral"],
                key="comp_sent"
            )

        # Apply company filter
        if company_choice != "All Companies":
            df_comp = df_comp[df_comp["company"] == company_choice]

        # Apply sentiment filter
        if comp_sent != "All":
            df_comp = df_comp[df_comp["sentiment"] == comp_sent]

        st.write(f"Showing **{len(df_comp)}** articles")
        st.divider()

        for _, row in df_comp.iterrows():
            emoji   = EMOJI.get(row["sentiment"], "")
            time    = pd.to_datetime(row["published_at"]).strftime("%d %b, %I:%M %p")
            company = row.get("company", "—")

            st.markdown(f"### {emoji} [{row['title']}]({row['url']})")
            st.caption(f" **{company}**  ·   {row['source']}  ·   {time}  ·  Sentiment: **{row['sentiment']}** (score: {row['score']})")
            st.divider()


# ════════════════════════════════════════════════════════════════════════════
#  TAB 3 — TECH & AI PULSE
# ════════════════════════════════════════════════════════════════════════════
with tab3:

    st.subheader(" Tech & AI Headlines")
    st.write("Latest from TechCrunch, The Verge, Wired, and Ars Technica — scored by sentiment.")

    # Filter only tech category articles
    df_tech = df[df["category"] == "tech"].copy()

    if df_tech.empty:
        st.warning("No tech news found. Check your notebook ran correctly.")
    else:
        # Source filter — lets user pick a specific tech publication
        col_x, col_y = st.columns(2)

        with col_x:
            tech_sent = st.selectbox(
                "Filter by Sentiment",
                ["All", "Positive", "Negative", "Neutral"],
                key="tech_sent"
            )

        with col_y:
            sources = ["All Sources"] + sorted(df_tech["source"].dropna().unique().tolist())
            source_choice = st.selectbox("Filter by Source", sources, key="tech_source")

        # Apply filters
        if tech_sent != "All":
            df_tech = df_tech[df_tech["sentiment"] == tech_sent]
        if source_choice != "All Sources":
            df_tech = df_tech[df_tech["source"] == source_choice]

        st.write(f"Showing **{len(df_tech)}** articles")
        st.divider()

        for _, row in df_tech.iterrows():
            emoji = EMOJI.get(row["sentiment"], "")
            time  = pd.to_datetime(row["published_at"]).strftime("%d %b, %I:%M %p")

            st.markdown(f"### {emoji} [{row['title']}]({row['url']})")
            st.caption(f" {row['source']}  ·   {time}  ·  Sentiment: **{row['sentiment']}** (score: {row['score']})")
            st.divider()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with NewsAPI · VADER Sentiment · Streamlit  |  Refresh: re-run the notebook → F5 this page")
