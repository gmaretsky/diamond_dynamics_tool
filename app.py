import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Diamond Dynamics", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #F4F2FF 0%, #FFFFFF 100%);
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.header {
    background: linear-gradient(135deg, #6C63FF 0%, #8A7DFF 100%);
    padding: 20px;
    border-radius: 14px;
    color: white;
    margin-bottom: 1.5rem;
}

h1 {
    font-size: 34px;
    font-weight: 700;
    margin: 0;
}

h2 {
    font-size: 22px;
    font-weight: 600;
    margin-top: 1.5rem;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #EAEAEA;
    text-align: center;
    margin-top: 1rem;
}

.metric-value {
    font-size: 44px;
    font-weight: 700;
    color: #6C63FF;
}

.insight-box {
    background: white;
    padding: 14px;
    border-radius: 10px;
    border: 1px solid #EAEAEA;
    margin-top: 15px;
}

.caption {
    font-size: 13px;
    color: #777;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
col1, col2 = st.columns([1, 8])

with col1:
    st.image("ddlogo.png", width=60)

with col2:
    st.markdown("""
    <div class="header">
        <h1>Diamond Dynamics</h1>
        <div style="font-size:14px; opacity:0.9;">
            Performance is not static. It evolves.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# TOOL (ONLY PAGE)
# =========================================================

# HOW IT WORKS
st.markdown("""
### How it works

Upload a game-by-game file and select a performance metric (OPS, OBP, etc.).

This tool tracks how performance evolves over time, not just what the final average is.
Each game is evaluated in the context of what came before it.

---

### How to read it

**Consistency Score**
- Measures how stable performance is across games  
- Lower = more consistent  
- Higher = more volatile  

**Adjustment Score**
- Measures how each game compares to recent performance  
- Positive = above recent trend  
- Negative = below recent trend  
- Near zero = in line with recent form  
""")

uploaded_file = st.file_uploader("Upload game-by-game CSV", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # Detect date column
    date_col = next((c for c in df.columns if "date" in c.lower()), None)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.sort_values(by=date_col)

    # Convert numeric safely
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # Remove unwanted columns
    numeric_cols = [col for col in numeric_cols if col not in ["Game", "Rolling Avg", "Adjustment", "Consistency"]]

    if len(numeric_cols) == 0:
        st.error("No usable numeric columns found.")
    else:
        metric = st.selectbox("Select Performance Metric", numeric_cols)

        df = df.dropna(subset=[metric]).reset_index(drop=True)
        df["Game"] = range(1, len(df) + 1)

        tool = st.radio("", ["Consistency", "Adjustment"], horizontal=True)

        # ================= CONSISTENCY =================
        if tool == "Consistency":

            df["Consistency"] = df[metric].expanding().std().fillna(0)
            latest = df["Consistency"].iloc[-1]

            st.markdown("<h2>Consistency Score</h2>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{round(latest, 3)}</div>
            </div>
            """, unsafe_allow_html=True)

            chart = alt.Chart(df).mark_line(point=True, color="#6C63FF").encode(
                x=alt.X("Game:O", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Consistency:Q"),
                tooltip=["Game", metric, "Consistency"]
            ).configure_axis(grid=False)

            st.altair_chart(chart, use_container_width=True)

            # Insight
            if latest < 0.05:
                insight = "Performance has been very stable. Results are repeating consistently."
            elif latest < 0.12:
                insight = "Performance shows some variation, but remains relatively steady."
            else:
                insight = "Performance has been volatile. Outcomes are fluctuating game to game."

            st.markdown(f"<div class='insight-box'><b>Insight:</b> {insight}</div>", unsafe_allow_html=True)

        # ================= ADJUSTMENT =================
        if tool == "Adjustment":

            df["Rolling Avg"] = df[metric].expanding().mean().shift(1)
            df["Adjustment"] = df[metric] - df["Rolling Avg"]
            df["Adjustment"] = df["Adjustment"].fillna(0)

            latest = df["Adjustment"].iloc[-1]

            st.markdown("<h2>Adjustment Score</h2>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{round(latest, 3)}</div>
            </div>
            """, unsafe_allow_html=True)

            base = alt.Chart(df)

            line = base.mark_line(point=True, color="#6C63FF").encode(
                x=alt.X("Game:O", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Adjustment:Q"),
                tooltip=["Game", metric, "Adjustment"]
            )

            zero = alt.Chart(pd.DataFrame({"y":[0]})).mark_rule(color="#999").encode(y="y:Q")

            chart = (line + zero).configure_axis(grid=False)

            st.altair_chart(chart, use_container_width=True)

            # Insight
            if latest > 0:
                insight = "Recent performance is trending above prior form."
            elif latest < 0:
                insight = "Recent performance is trending below prior form."
            else:
                insight = "Performance is holding steady relative to recent games."

            st.markdown(f"<div class='insight-box'><b>Insight:</b> {insight}</div>", unsafe_allow_html=True)

else:
    st.write("Upload a CSV to begin.")
