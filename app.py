import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from inference import (
    predict_tx,
    plot_3d_tx_ego,
    neighbor_risk_distribution,
    overall_risk_distribution,
    ego_risk_distribution,
)

# ----------------------------------------------------------
# PAGE SETUP
# ----------------------------------------------------------
st.set_page_config(page_title="Bitcoin Transaction Risk Explorer", layout="wide")

# ----------------------------------------------------------
# BEAUTIFUL UI CSS (animations + modern visuals)
# ----------------------------------------------------------
st.markdown("""
<style>
body {
    font-family: 'Inter', sans-serif;
}
/* MAIN TITLE */
h1 {
    background: linear-gradient(90deg, #00eaff, #6f00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: -1px;
}
/* SECTION HEADERS */
h3 {
    color: #dff6ff;
    font-weight: 700;
    margin-top: 30px;
}
/* Metric Cards */
.metric-card {
    background: rgba(255, 255, 255, 0.03);
    padding: 16px;
    border-radius: 14px;
    border: 1px solid rgba(0, 200, 255, 0.15);
    backdrop-filter: blur(10px);
    transition: 0.25s ease;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 200, 255, 0.12);
}
/* Analyze button */
.stButton > button {
    background: linear-gradient(90deg, #00c6ff, #7d2cff);
    color: white;
    padding: 10px 26px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 700;
    border: none;
    transition: 0.22s ease-in-out;
    box-shadow: 0 0 12px rgba(0, 200, 255, 0.3);
}
.stButton > button:hover {
    transform: scale(1.07);
    box-shadow: 0 0 22px rgba(0, 200, 255, 0.45);
}
/* Sidebar styling */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.02);
    border-right: 1px solid rgba(0,200,255,0.1);
}
.sidebar-link {
    color: #4db8ff !important;
    font-weight: 700;
}
/* Text fade-in animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(8px);}
    to {opacity: 1; transform: translateY(0);}
}
.fade {
    animation: fadeIn 0.6s ease forwards;
}
/* Slider */
.stSlider > div > div > div {
    background: linear-gradient(90deg, #00d4ff, #6f00ff) !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# HEADER
# ----------------------------------------------------------
st.markdown("<h1 class='fade'>Bitcoin Transaction Risk Explorer</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="fade" style='color:#b9d6e8; font-size:16px; margin-bottom:25px;'>
AI-powered forensic intelligence. Predict illicit risk, analyze network behavior, and visualize suspicious transaction activity in 3D.
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# Sidebar helper: attractive bar chart renderer
# ----------------------------------------------------------
def render_sidebar_bar_chart(counts: dict):
    """Render an attractive Plotly bar chart in the sidebar with labels outside (avoid clipping)."""
    if not counts:
        st.sidebar.write("No risk data available.")
        return

    df = pd.DataFrame({
        "Risk": list(counts.keys()),
        "Count": list(counts.values())
    })

    # keep consistent order: Safe, High, Low, Medium (if present)
    desired_order = ["Safe", "High", "Low", "Medium"]
    df['Risk'] = pd.Categorical(df['Risk'], categories=[r for r in desired_order if r in df['Risk'].unique()], ordered=True)
    df = df.sort_values('Risk')

    fig = px.bar(
        df,
        x="Risk",
        y="Count",
        text="Count",
        color="Risk",
        color_discrete_map={
            "Safe": "#4da3ff",
            "High": "#ff2e63",
            "Low": "#00e0c7",
            "Medium": "#ffa41b"
        }
    )

    fig.update_traces(
        texttemplate="%{text:,}",       # format with commas
        textposition="outside",        # move label outside bar to prevent clipping
        cliponaxis=False,
        marker=dict(line=dict(color="rgba(255,255,255,0.55)", width=1.5))
    )

    fig.update_layout(
        height=340,
        margin=dict(l=10, r=10, t=8, b=8),
        yaxis_title="Count",
        xaxis_title="Risk",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )

    st.sidebar.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------
# SIDEBAR — Global Risk Distribution
# ----------------------------------------------------------
st.sidebar.header("📊 Global Risk Overview")

overall_counts = overall_risk_distribution()

# metric cards
if overall_counts:
    total = sum(overall_counts.values())
    for k, v in overall_counts.items():
        st.sidebar.markdown(
            f"""
            <div class='metric-card'>
                <div style="font-size:16px; font-weight:700">{k}</div>
                <div style="font-size:22px; margin-top:6px">
                    {v:,} <span style='color:#9fbcd6; font-size:13px;'>({v/total*100:.1f}%)</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Render improved Plotly bar chart (fixes large-label clipping)
    render_sidebar_bar_chart(overall_counts)

else:
    st.sidebar.write("No risk data available.")

st.sidebar.markdown("---")

# Dataset Link
st.sidebar.markdown("""
🔗 **Dataset Source:**  
[Open Bitcoin Fraud Dataset →](https://huggingface.co/datasets/Nikhil0702/Bitcoin_dataset/tree/main)
""")

# ----------------------------------------------------------
# INPUTS
# ----------------------------------------------------------
st.subheader("🔍 Analyze a Transaction")

tx_input = st.text_input("Enter transaction ID (txId)", value="78144215")

col_h1, col_h2 = st.columns(2)
with col_h1:
    hops = st.slider("Ego-graph hops", 1, 4, 2)
with col_h2:
    max_nodes = st.slider("Max nodes in ego graph", 50, 800, 400, step=50)

# ----------------------------------------------------------
# ANALYSIS LOGIC
# ----------------------------------------------------------
if st.button("Analyze"):
    try:
        try:
            txid = int(tx_input)
        except:
            txid = tx_input

        info = predict_tx(txid)

        st.markdown("### Prediction Summary")

        c1, c2, c3, c4, c5 = st.columns(5)

        # Metric function
        def card(col, title, value):
            col.markdown(
                f"""
                <div class="metric-card fade">
                    <div style='color:#9fbcd6; font-size:13px;'>{title}</div>
                    <div style='font-size:22px; font-weight:700; margin-top:6px'>{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        card(c1, "Transaction ID", info["txId"])
        card(c2, "Illicit Probability", f"{info['proba_illicit']:.6f}")
        card(c3, "Risk Bucket", info["risk_bucket"])
        card(c4, "Degree", info["degree"])
        card(c5, "Original Class", info["class"])

        st.markdown("---")

        # ----------------------------------------------------
        # Neon Donut Chart (Ego Risk)
        # ----------------------------------------------------
        st.markdown("### 🥧 Ego-Network Risk Composition")

        ego_counts = ego_risk_distribution(txid, hops=hops, max_nodes=max_nodes)

        if ego_counts:
            labels = list(ego_counts.keys())
            values = list(ego_counts.values())

            color_map = {
                "High": "#ff2e63",
                "Medium": "#ffa41b",
                "Low": "#00e0c7",
                "Safe": "#5596ff"
            }
            colors = [color_map.get(r, "#9fbcd6") for r in labels]

            pie_fig = go.Figure(
                data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.55,
                    hoverinfo="label+percent+value",
                    textinfo="percent",
                    textfont=dict(size=14, color="white"),
                    marker=dict(
                        colors=colors,
                        line=dict(color="rgba(255,255,255,0.18)", width=2)
                    ),
                    sort=False
                )]
            )

            pie_fig.update_layout(
                title="Risk Distribution (Ego Network)",
                title_font=dict(color="white"),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                annotations=[
                    dict(
                        text="EGO",
                        x=0.5, y=0.5,
                        font=dict(size=22, color="white"),
                        showarrow=False
                    )
                ],
                margin=dict(l=10, r=10, t=60, b=10),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="#dff8ff")
                )
            )

            st.plotly_chart(pie_fig, use_container_width=True)

        else:
            st.info("No ego-network risk data available.")

        st.markdown("---")

        # ------------------------------------------------------
        # NEIGHBOR RISK
        # ------------------------------------------------------
        st.markdown("### 📌 Neighbor Risk Distribution")
        nb_counts = neighbor_risk_distribution(txid)

        if nb_counts:
            st.bar_chart(pd.Series(nb_counts))
        else:
            st.info("No neighbors found for this transaction.")

        st.markdown("---")

        # ------------------------------------------------------
        # 3D NETWORK GRAPH
        # ------------------------------------------------------
        st.markdown("### 🌐 3D Ego Graph")
        fig = plot_3d_tx_ego(txid, hops=hops, max_nodes=max_nodes)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Unexpected error: {e}")
