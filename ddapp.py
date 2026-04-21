import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Diamond Dynamics",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ==================================================
# STYLING (Diamond Dynamics purple/black aesthetic)
# ==================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #0a0a0f, #151520);
    color: white;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #120f1d 0%, #181325 100%);
}
.hero {
    background: linear-gradient(135deg, rgba(124,58,237,0.24), rgba(255,255,255,0.05));
    padding: 1.8rem;
    border-radius: 18px;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(167,139,250,0.20);
}
.section-box {
    background: rgba(255,255,255,0.04);
    padding: 1.15rem;
    border-radius: 16px;
    margin-bottom: 1rem;
}
.insight-box {
    background: rgba(124,58,237,0.18);
    border-left: 4px solid #a78bfa;
    padding: 1rem;
    border-radius: 12px;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}
.small-tag {
    display: inline-block;
    padding: 0.28rem 0.7rem;
    border-radius: 999px;
    background: rgba(167,139,250,0.14);
    border: 1px solid rgba(167,139,250,0.18);
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
    color: #f1ebff;
    font-size: 0.82rem;
    font-weight: 600;
}
.metric-caption {
    color: #d9d1ff;
    font-size: 0.9rem;
}
.note-text {
    color: #ddd6fe;
    line-height: 1.65;
}
.subtle-divider {
    border-top: 1px solid rgba(167,139,250,0.18);
    margin-top: 1rem;
    margin-bottom: 1rem;
}
ul, ol {
    margin-top: 0.35rem;
}
h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.title("Diamond Dynamics")
    page = st.radio("Navigate", ["Tool", "How It Works", "Data Format"])

    st.markdown("---")
    st.markdown("### Score Guide")
    st.markdown("""
**Consistency**
- **0.70 - 1.00** = High
- **0.40 - 0.69** = Moderate
- **Below 0.40** = Low

**Adjustment**
- **0.70 - 1.00** = Strong
- **0.50 - 0.69** = Moderate
- **0.35 - 0.49** = Stable / Neutral
- **Below 0.35** = Low Activity
""")
# ==================================================
# STYLING (Diamond Dynamics purple/black aesthetic)
# ==================================================
st.markdown("""
<style>

/* ===== BASE APP ===== */
.stApp {
    background: linear-gradient(180deg, #0a0a0f, #151520);
    color: white;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #120f1d 0%, #181325 100%);
}

/* ===== HERO ===== */
.hero {
    background: linear-gradient(135deg, rgba(124,58,237,0.24), rgba(255,255,255,0.05));
    padding: 1.8rem;
    border-radius: 18px;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(167,139,250,0.20);
}

/* ===== SECTIONS ===== */
.section-box {
    background: rgba(255,255,255,0.04);
    padding: 1.15rem;
    border-radius: 16px;
    margin-bottom: 1rem;
}

.insight-box {
    background: rgba(124,58,237,0.18);
    border-left: 4px solid #a78bfa;
    padding: 1rem;
    border-radius: 12px;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}

/* ===== TAGS ===== */
.small-tag {
    display: inline-block;
    padding: 0.28rem 0.7rem;
    border-radius: 999px;
    background: rgba(167,139,250,0.14);
    border: 1px solid rgba(167,139,250,0.18);
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
    color: #f1ebff;
    font-size: 0.82rem;
    font-weight: 600;
}

/* ===== TEXT ===== */
.metric-caption {
    color: #d9d1ff;
    font-size: 0.9rem;
}

.note-text {
    color: #ddd6fe;
    line-height: 1.65;
}

h1, h2, h3 {
    color: white;
}

/* ===== FIX FADED RESULTS ===== */
[data-testid="stMetricLabel"] {
    color: #E5E5FF !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 700;
}

[data-testid="stCaption"] {
    color: #CFCFFF !important;
}

/* ===== FIX SIDEBAR ===== */
section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stRadio"] label {
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)
# ==================================================
# HELPERS
# ==================================================
def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()
    return df

def parse_time(df: pd.DataFrame, col: str):
    working = df.copy()
    numeric = pd.to_numeric(working[col], errors="coerce")
    if numeric.notna().sum() > len(working) * 0.7:
        working[col] = numeric.astype(int)
        working = working.dropna(subset=[col]).sort_values(col).reset_index(drop=True)
        return working, "game"
    working[col] = pd.to_datetime(working[col], errors="coerce")
    working = working.dropna(subset=[col]).sort_values(col).reset_index(drop=True)
    return working, "date"

def format_x_values(values: pd.Series, axis_type: str):
    if axis_type == "game":
        return values.astype(int).tolist()
    return pd.to_datetime(values).dt.strftime("%Y-%m-%d").tolist()

def min_max_normalize(values: np.ndarray) -> np.ndarray:
    if len(values) == 0:
        return np.array([])
    min_val = np.min(values)
    max_val = np.max(values)
    if max_val == min_val:
        return np.ones(len(values))
    return (values - min_val) / (max_val - min_val)

# ==================================================
# CORE LOGIC (quality-aware consistency)
# ==================================================
def calculate_quality_weighted_consistency(values: np.ndarray) -> float:
    if len(values) == 0:
        return np.nan
    if len(values) == 1:
        return 0.50

    values = np.array(values, dtype=float)

    # --- STEP 1: Measure spread (this is the core fix) ---
    std_dev = np.std(values)
    value_range = np.max(values) - np.min(values)

    if value_range == 0:
        spread_score = 1.0
    else:
        spread_score = 1 - (std_dev / value_range)

    spread_score = max(0.0, min(1.0, spread_score))

    # --- STEP 2: Reward tight clustering around recent performance ---
    recent_window = values[-min(5, len(values)):]
    recent_std = np.std(recent_window)

    if value_range == 0:
        recent_stability = 1.0
    else:
        recent_stability = 1 - (recent_std / value_range)

    recent_stability = max(0.0, min(1.0, recent_stability))

    # --- STEP 3: Light quality influence (NOT dominant) ---
    quality_scale = min_max_normalize(values)
    avg_quality = float(np.mean(quality_scale))

    # --- FINAL BLEND ---
    consistency = (
        0.50 * spread_score +      # overall tightness
        0.30 * recent_stability +  # recent stability
        0.20 * avg_quality        # slight performance reward
    )

    return float(max(0.0, min(1.0, consistency)))

def calculate_adjustment_score(values: np.ndarray) -> float:
    if len(values) == 0:
        return np.nan
    if len(values) == 1:
        return 0.50

    step_scores = [0.50]
    for i in range(1, len(values)):
        prior_values = values[:i]
        prior_baseline = float(np.mean(prior_values))
        current_dev = abs(values[i] - prior_baseline)
        prior_spread = float(np.max(np.abs(prior_values - prior_baseline))) if len(prior_values) > 0 else 0.0
        scale = max(prior_spread, current_dev)

        if scale == 0:
            step_score = 1.0
        else:
            step_score = max(0.0, min(1.0, 1 - (current_dev / scale)))

        step_scores.append(step_score)

    return float(np.mean(step_scores))

def calculate_full_sample(df: pd.DataFrame, value_col: str):
    working = df.copy()
    working[value_col] = pd.to_numeric(working[value_col], errors="coerce")
    working = working.dropna(subset=[value_col]).reset_index(drop=True)

    baseline = float(working[value_col].mean())
    working["Deviation"] = (working[value_col] - baseline).abs()

    values = working[value_col].to_numpy(dtype=float)
    consistency = calculate_quality_weighted_consistency(values)
    adjustment = calculate_adjustment_score(values)

    return consistency, adjustment, baseline, working

def build_trends(df: pd.DataFrame, time_col: str, value_col: str) -> pd.DataFrame:
    time_vals = []
    baseline_vals = []
    consistency_vals = []
    adjustment_vals = []

    for i in range(1, len(df) + 1):
        temp = df.iloc[:i].copy()
        c, a, b, _ = calculate_full_sample(temp, value_col)
        time_vals.append(df[time_col].iloc[i - 1])
        baseline_vals.append(b)
        consistency_vals.append(c)
        adjustment_vals.append(a)

    return pd.DataFrame({
        time_col: time_vals,
        "Baseline": baseline_vals,
        "Consistency": consistency_vals,
        "Adjustment": adjustment_vals
    })

# ==================================================
# INTERPRETATION & INSIGHTS
# ==================================================
def classify_consistency(score: float) -> str:
    if pd.isna(score):
        return "Not enough data yet"
    if score >= 0.70:
        return "High"
    if score >= 0.40:
        return "Moderate"
    return "Low"

def classify_adjustment(score: float) -> str:
    if pd.isna(score):
        return "Not enough data yet"
    if score >= 0.70:
        return "Strong"
    if score >= 0.50:
        return "Moderate"
    if score >= 0.35:
        return "Stable / Neutral"

    return "Low Activity"

def overall_profile(consistency: float, adjustment: float) -> str:
    if pd.isna(consistency) and pd.isna(adjustment):
        return "Early sample"
    if consistency >= 0.70:
        if adjustment >= 0.70:
            return "Stable and resilient"
        return "Stable"
    if consistency >= 0.50:
        if adjustment >= 0.70:
            return "Stable with adaptability"
        return "Generally stable"
    if consistency >= 0.40:
        return "Moderately variable"

    return "Highly variable"
def build_summary(consistency: float, adjustment: float, baseline: float, stat_name: str) -> str:
    profile = overall_profile(consistency, adjustment)
    consistency_text = classify_consistency(consistency)
    adjustment_text = classify_adjustment(adjustment)

    return (
        f"This player grades as <b>{profile.lower()}</b> over the uploaded sample. "
        f"The selected stat has a baseline of <b>{baseline:.3f}</b> in <b>{stat_name}</b>, "
        f"which represents the player's typical level in this dataset. "
        f"The current consistency reading is <b>{consistency_text.lower()}</b>, "
        f"and the current adjustment reading is <b>{adjustment_text.lower()}</b>."
    )

def trend_direction_text(series: pd.Series, label: str) -> str:
    valid = series.dropna()
    if len(valid) < 3:
        return f"There is not enough history yet to evaluate the player's {label.lower()} trend."
    start = float(valid.iloc[0])
    mid = float(valid.iloc[len(valid)//2])
    end = float(valid.iloc[-1])
    # Upward pattern
    if end > start and end >= mid:
        return f"The player's {label.lower()} trend shows gradual improvement over the sample."
    # Early drop then stabilize/recover
    if end < start and end >= mid:
        return f"The player's {label.lower()} trend dipped early but stabilized over time."
    # Continued decline
    if end < start and end < mid:
        return f"The player's {label.lower()} trend shows a downward pattern over the sample."
    # Default: stable
    return f"The player's {label.lower()} trend has remained relatively stable with minor fluctuations."

def stat_insight(calc_df: pd.DataFrame, value_col: str, baseline: float) -> str:
    latest = float(calc_df[value_col].iloc[-1])
    first = float(calc_df[value_col].iloc[0])
    recent_avg = float(calc_df[value_col].tail(min(5, len(calc_df))).mean())

    direction = "higher" if latest > first else "lower" if latest < first else "the same"
    recent_vs_baseline = "above" if recent_avg > baseline else "below" if recent_avg < baseline else "in line with"

    return (
    f"The player's selected stat begins at <b>{first:.3f}</b> and ends at <b>{latest:.3f}</b>, "
    f"so the latest value is <b>{direction}</b> than the first value in the sample. "
    f"The recent short-window average is <b>{recent_avg:.3f}</b>, which sits <b>{recent_vs_baseline}</b> "
    f"the overall baseline of <b>{baseline:.3f}</b>."
)

# ==================================================
# CHARTING (NO GRIDLINES)
# ==================================================
def plot_line(x, y, title: str, xlabel: str, ylabel: str, baseline=None, y_limits=None):
    plot_df = pd.DataFrame({"x": x, "y": y})

    if xlabel == "Game":
        plot_df["x"] = pd.to_numeric(plot_df["x"], errors="coerce")
        x_encoding = alt.X("x:Q", title=xlabel, axis=alt.Axis(format="d", grid=False))
        tooltip_x = alt.Tooltip("x:Q", title=xlabel)
    else:
        plot_df["x"] = pd.to_datetime(plot_df["x"], errors="coerce")
        x_encoding = alt.X("x:T", title=xlabel, axis=alt.Axis(grid=False))
        tooltip_x = alt.Tooltip("x:T", title=xlabel)

    y_encoding = alt.Y("y:Q", title=ylabel, axis=alt.Axis(grid=False))
    if y_limits is not None:
        y_encoding = alt.Y("y:Q", title=ylabel, scale=alt.Scale(domain=list(y_limits)), axis=alt.Axis(grid=False))

    line = alt.Chart(plot_df).mark_line(point=True).encode(
        x=x_encoding,
        y=y_encoding,
        tooltip=[tooltip_x, alt.Tooltip("y:Q", title=ylabel, format=".3f")]
    ).properties(title=title, height=350)

    if baseline is not None:
        baseline_df = pd.DataFrame({"baseline": [baseline]})
        rule = alt.Chart(baseline_df).mark_rule(strokeDash=[6, 4]).encode(y=alt.Y("baseline:Q"))
        chart = (line + rule).interactive()
    else:
        chart = line.interactive()

    st.altair_chart(chart, use_container_width=True)

# ==================================================
# TOOL PAGE (logo + no baseball-context blocks)
# ==================================================
if page == "Tool":
    col_logo, col_title = st.columns([2, 6])

    with col_logo:
        st.image("ddlogo.png", width=260)

    with col_title:
        st.markdown("""
        <div class="hero">
            <h1 style="margin-bottom:0;">Diamond Dynamics Tool</h1>
            <p style="margin-top:5px;">
Track how a player’s performance evolves over time through consistency and adjustment trends.
</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-box">
        <b>What this tool is measuring</b><br><br>
        This tool evaluates how a player’s performance evolves over time using a selected stat (such as OPS, OBP, SLG, ERA, or WHIP):
        <ul>
            <li><b>Consistency</b> — how consistently the player performs over time</li>
            <li><b>Adjustment</b> — how the player responds after performance changes</li>
        </ul>
        <span class="small-tag">Player-focused evaluation</span>
        <span class="small-tag">Game-by-game trends</span>
        <span class="small-tag">Date or Game format</span>
        <span class="small-tag">CSV or Excel</span>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

    if uploaded is not None:
        raw_df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
        raw_df = clean_columns(raw_df)

        st.subheader("Data Preview")
        st.dataframe(raw_df, use_container_width=True)

        cols = raw_df.columns.tolist()
        c1, c2 = st.columns(2)
        with c1:
            time_col = st.selectbox("Select the sequence column (Game or Date)", cols)
        with c2:
            value_col = st.selectbox("Select the stat column to analyze", cols)

        df, axis_type = parse_time(raw_df, time_col)
        consistency, adjustment, baseline, calc_df = calculate_full_sample(df, value_col)
        trend_df = build_trends(calc_df, time_col, value_col)

        trend_x_labels = format_x_values(trend_df[time_col], axis_type)

        st.subheader("Results")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Baseline", f"{baseline:.3f}")
        with m2:
            st.metric("Consistency", "N/A" if pd.isna(consistency) else f"{consistency:.2f}")
            st.caption(classify_consistency(consistency))
        with m3:
            st.metric("Adjustment", "N/A" if pd.isna(adjustment) else f"{adjustment:.2f}")
            st.caption(classify_adjustment(adjustment))
        st.markdown("---")

        report_text = f"""
DIAMOND DYNAMICS REPORT

Consistency: {consistency:.2f}
Adjustment: {adjustment:.2f}
Baseline: {baseline:.3f}

PROFILE SUMMARY:
{build_summary(consistency, adjustment, baseline, value_col)}

DATA INSIGHT:
{stat_insight(calc_df, value_col, baseline)}
"""

        st.download_button(
            label="Download Diamond Dynamics Report",
            data=report_text,
            file_name="diamond_dynamics_report.txt",
            mime="text/plain"
        )
        
        st.markdown(f"""
        <div class="insight-box">
            <b>Profile Summary</b><br><br>
            {build_summary(consistency, adjustment, baseline, value_col)}
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Consistency Trend")
        plot_line(
            x=trend_x_labels,
            y=trend_df["Consistency"],
            title="Consistency Trend",
            xlabel="Game" if axis_type == "game" else "Date",
            ylabel="Consistency",
            y_limits=(0, 1)
        )
        st.write(trend_direction_text(trend_df["Consistency"], "Consistency"))

        st.subheader("Adjustment Trend")
        plot_line(
            x=trend_x_labels,
            y=trend_df["Adjustment"],
            title="Adjustment Trend",
            xlabel="Game" if axis_type == "game" else "Date",
            ylabel="Adjustment",
            y_limits=(0, 1)
        )
        st.write(trend_direction_text(trend_df["Adjustment"], "Adjustment"))

        st.markdown(f"""
<div class="insight-box">
    <b>Data Insight</b><br><br>
    {stat_insight(calc_df, value_col, baseline)}
</div>
""", unsafe_allow_html=True)

# ==================================================
# HOW IT WORKS PAGE
# ==================================================
elif page == "How It Works":
    st.markdown("""
    <div class="hero">
        <h1>How It Works</h1>
        <p>A detailed guide to using FanGraphs-style data in the Diamond Dynamics tool.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-box">
        <b>Step 1:</b> Go to FanGraphs and find a player's game log.
    </div>
    <div class="section-box">
        <b>Step 2:</b> Copy the Game/Date column and a rate-based stat (OPS, OBP, SLG, etc.).
    </div>
    <div class="section-box">
        <b>Step 3:</b> Paste into Excel and save as CSV.
    </div>
    <div class="section-box">
        <b>Step 4:</b> Upload and select your columns.
    </div>
    <div class="section-box">
        <b>Step 5:</b> The tool builds a baseline and evaluates consistency and adjustment game by game.
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# DATA FORMAT PAGE
# ==================================================
elif page == "Data Format":
    st.markdown("""
    <div class="hero">
        <h1>Data Format</h1>
        <p>How to structure your file.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
<div class="section-box">
    The tool is flexible to sample size, allowing users to upload as much or as little data as they choose, with calculations updating as data accumulates.
</div>
""", unsafe_allow_html=True)

    st.subheader("Example (Game)")
    st.dataframe(pd.DataFrame({
        "Game": [1, 2, 3],
        "OPS": [0.000, 0.541, 0.800]
    }))

    st.subheader("Example (Date)")
    st.dataframe(pd.DataFrame({
        "Date": ["2026-03-01", "2026-03-02", "2026-03-03"],
        "OBP": [0.300, 0.400, 0.350]
    }))
