import streamlit as st
import pandas as pd
from nba_api.stats.static import players

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="NBA Player Performance Risk Engine",
    page_icon="🏀",
    layout="wide"
)

# ---------- HELPERS ----------
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("reports/fatigue_predictions.csv")
    df["game_date"] = pd.to_datetime(df["game_date"])
    return df


def get_player_id(player_name: str):
    matches = players.find_players_by_full_name(player_name)
    if matches:
        return matches[0]["id"]
    return None


def get_headshot_url(player_name: str):
    player_id = get_player_id(player_name)
    if player_id:
        return f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png"
    return None


def risk_label(score: float) -> str:
    if score >= 75:
        return "🔴 High"
    elif score >= 40:
        return "🟡 Medium"
    return "🟢 Low"


def risk_color(score: float) -> str:
    if score >= 75:
        return "#ff4b4b"
    elif score >= 40:
        return "#f0b429"
    return "#22c55e"


# ---------- STYLING ----------
st.markdown(
    """
    <style>
    .main {
        background-color: #0f172a;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .metric-card {
        background: #111827;
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #1f2937;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
        min-height: 110px;
    }
    .section-card {
        background: #111827;
        padding: 1.25rem;
        border-radius: 16px;
        border: 1px solid #1f2937;
        margin-top: 1rem;
    }
    .small-label {
        font-size: 0.9rem;
        color: #9ca3af;
        margin-bottom: 0.2rem;
    }
    .big-number {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff !important;
        line-height: 1.2;
    }
    .title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        color: #475569;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- LOAD DATA ----------
df = load_data()
players_list = sorted(df["player_name"].unique())

# ---------- SIDEBAR ----------
st.sidebar.title("Controls")
selected_player = st.sidebar.selectbox("Select Player", players_list)
show_top_risk = st.sidebar.checkbox("Show top risky games", True)
show_feature_chart = st.sidebar.checkbox("Show feature importance", True)

player_df = df[df["player_name"] == selected_player].sort_values("game_date")

# ---------- SAFETY CHECK ----------
if player_df.empty:
    st.warning("No data available for this player.")
    st.stop()

latest = player_df.iloc[-1]

# ---------- HEADER ----------
col1, col2 = st.columns([1, 4])

with col1:
    img = get_headshot_url(selected_player)
    if img:
        st.image(img, width=140)

with col2:
    st.markdown(
        '<div class="title">🏀 NBA Player Performance Risk Engine</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="subtitle">Tracking fatigue risk, dip probability, and workload trends for <b>{selected_player}</b>.</div>',
        unsafe_allow_html=True
    )

# ---------- METRICS ----------
m1, m2, m3, m4 = st.columns(4)

m1.markdown(
    f"""
    <div class="metric-card">
        <div class="small-label">Fatigue Risk Score</div>
        <div class="big-number">{latest['fatigue_risk_score']:.1f}</div>
    </div>
    """,
    unsafe_allow_html=True
)

m2.markdown(
    f"""
    <div class="metric-card">
        <div class="small-label">Dip Probability</div>
        <div class="big-number">{latest['dip_probability'] * 100:.1f}%</div>
    </div>
    """,
    unsafe_allow_html=True
)

pred = "⚠️ Dip" if latest["predicted_performance_dip"] == 1 else "✅ Stable"

m3.markdown(
    f"""
    <div class="metric-card">
        <div class="small-label">Latest Prediction</div>
        <div class="big-number">{pred}</div>
    </div>
    """,
    unsafe_allow_html=True
)

color = risk_color(latest["fatigue_risk_score"])
label = risk_label(latest["fatigue_risk_score"])

m4.markdown(
    f"""
    <div class="metric-card">
        <div class="small-label">Risk Level</div>
        <div class="big-number" style="color:{color};">{label}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- RISK GAUGE ----------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Current Fatigue Risk Gauge")

score = float(latest["fatigue_risk_score"])
risk_value = score / 100

# dynamic color
if score >= 75:
    color = "red"
elif score >= 40:
    color = "orange"
else:
    color = "green"

st.progress(risk_value)

st.markdown(
    f"<p style='color:{color}; font-weight:600;'>Current fatigue risk score: {score:.1f} / 100</p>",
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- CHART + SNAPSHOT ----------
left, right = st.columns([2, 1])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Fatigue Risk Over Time")
    chart_df = player_df.sort_values("game_date").set_index("game_date")[["fatigue_risk_score"]]
    st.line_chart(chart_df)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Latest Game Snapshot")
    st.write(f"Date: {latest['game_date'].date()}")
    st.write(f"Minutes: {latest['min']}")
    st.write(f"Points: {latest['pts']}")
    st.write(f"Assists: {latest['ast']}")
    st.write(f"Rebounds: {latest['reb']}")
    st.write(f"Days Rest: {latest['days_rest']}")
    st.write(f"Back-to-Back: {'Yes' if latest['is_back_to_back'] == 1 else 'No'}")
    st.write(f"Workload Score: {latest['workload_score']:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- TOP RISK ----------
if show_top_risk:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader(f"Top Risk Games for {selected_player}")

    sort_option = st.selectbox(
        "Sort top games by",
        ["fatigue_risk_score", "dip_probability", "pts", "workload_score"],
        index=0
    )

    top = player_df.sort_values(sort_option, ascending=False).head(10).copy()
    top["dip_probability"] = (top["dip_probability"] * 100).round(1)

    st.dataframe(
        top[
            [
                "game_date",
                "fatigue_risk_score",
                "dip_probability",
                "predicted_performance_dip",
                "min",
                "pts",
                "days_rest",
                "is_back_to_back",
                "workload_score"
            ]
        ],
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RECENT GAMES ----------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Recent Games")
st.dataframe(
    player_df.sort_values("game_date", ascending=False).head(10),
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- FEATURE IMPORTANCE ----------
if show_feature_chart:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Model Feature Importance")
    st.image("reports/feature_importance.png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "Built by Myke | NBA Fatigue Risk Engine | Python • SQL • Machine Learning • Streamlit"
)