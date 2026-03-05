import pandas as pd
import numpy as np
import networkx as nx
import joblib
import plotly.graph_objects as go
from huggingface_hub import hf_hub_download

# ============================================================
# 1. REMOTE DATASET PATHS (HuggingFace Dataset Repo)
# ============================================================

REPO_ID = "Nikhil0702/Bitcoin_dataset"

FEATURES_REMOTE = "data/elliptic_txs_features.csv"
CLASSES_REMOTE  = "data/elliptic_txs_classes.csv"
EDGES_REMOTE    = "data/elliptic_txs_edgelist.csv"

MODEL_PATH = "models/lightgbm_final_model.pkl"


# ============================================================
# 2. DOWNLOAD FILES FROM HUGGINGFACE DATASET REPO
# ============================================================

def download_file(path):
    return hf_hub_download(
        repo_id=REPO_ID,
        filename=path,
        repo_type="dataset",
        force_download=False
    )

features_local = download_file(FEATURES_REMOTE)
classes_local  = download_file(CLASSES_REMOTE)
edges_local    = download_file(EDGES_REMOTE)


# ============================================================
# 3. LOAD DATA
# ============================================================
features_raw = pd.read_csv(features_local, header=None)

num_cols = features_raw.shape[1]
num_feats = num_cols - 2

feat_cols = [f"f_{i}" for i in range(1, num_feats + 1)]
rename_map = {0: "txId", 1: "time_step"}
rename_map.update({i + 2: feat_cols[i] for i in range(num_feats)})

features_df = features_raw.rename(columns=rename_map)

classes_df = pd.read_csv(classes_local)
classes_df = classes_df.rename(columns={
    classes_df.columns[0]: "txId",
    classes_df.columns[1]: "class"
})

edges_df = pd.read_csv(edges_local)
edges_df = edges_df.rename(columns={
    edges_df.columns[0]: "src",
    edges_df.columns[1]: "dst"
})

features_df["txId"] = features_df["txId"].astype(int)
classes_df["txId"]  = classes_df["txId"].astype(int)
edges_df["src"]     = edges_df["src"].astype(int)
edges_df["dst"]     = edges_df["dst"].astype(int)

data_df = features_df.merge(classes_df, on="txId", how="left")


# ============================================================
# 4. LOAD MODEL + PROBABILITIES
# ============================================================
model = joblib.load(MODEL_PATH)

X_full = data_df[feat_cols].values.astype("float32")
proba = model.predict_proba(X_full)[:, 1]

data_df["proba_illicit"] = proba


# ============================================================
# 5. RISK BUCKET
# ============================================================
def risk_bucket(p):
    if p >= 0.90: return "High"
    if p >= 0.75: return "Medium"
    if p >= 0.50: return "Low"
    return "Safe"

data_df["risk_bucket"] = data_df["proba_illicit"].apply(risk_bucket)


# ============================================================
# 6. GRAPH BUILD
# ============================================================
G_full = nx.Graph()
G_full.add_edges_from(edges_df[["src", "dst"]].itertuples(index=False, name=None))

degree_map = dict(G_full.degree())
data_df["degree"] = data_df["txId"].map(degree_map).fillna(0).astype(int)

proba_map  = data_df.set_index("txId")["proba_illicit"].to_dict()
bucket_map = data_df.set_index("txId")["risk_bucket"].to_dict()

class_raw = data_df.set_index("txId")["class"].to_dict()
CLASS_LABELS = {1: "Illicit", 2: "Licit", 0: "Unknown"}
class_map = {tx: CLASS_LABELS.get(lbl, "Unknown") for tx, lbl in class_raw.items()}


# ============================================================
# 7. PREDICT ONE TX
# ============================================================
def predict_tx(txid):
    txid = int(txid)

    if txid not in proba_map:
        raise ValueError(f"txId {txid} not found")

    return {
        "txId": txid,
        "proba_illicit": float(proba_map[txid]),
        "risk_bucket": bucket_map.get(txid, "Safe"),
        "degree": int(degree_map.get(txid, 0)),
        "class": class_map.get(txid, "Unknown")
    }


# ============================================================
# 8. NEIGHBOR RISK
# ============================================================
def neighbor_risk_distribution(txid):
    txid = int(txid)

    if txid not in G_full:
        return {}

    nbrs = list(G_full.neighbors(txid))
    if not nbrs:
        return {}

    df = data_df.set_index("txId").loc[nbrs]
    return df["risk_bucket"].value_counts().to_dict()


# ============================================================
# 9. OVERALL RISK
# ============================================================
def overall_risk_distribution():
    return data_df["risk_bucket"].value_counts().to_dict()


# ============================================================
# 10. EGO NETWORK RISK
# ============================================================
def ego_risk_distribution(txid, hops=2, max_nodes=400):
    txid = int(txid)

    ego = nx.ego_graph(G_full, txid, radius=hops)

    if ego.number_of_nodes() > max_nodes:
        nodes = list(ego.nodes())
        nodes.remove(txid)
        top = sorted(nodes, key=lambda n: ego.degree[n], reverse=True)
        ego = ego.subgraph([txid] + top[:max_nodes - 1])

    bucket_list = [bucket_map.get(n, "Safe") for n in ego.nodes()]
    return pd.Series(bucket_list).value_counts().to_dict()


# ============================================================
# 11. FINAL 3D GRAPH (UPDATED)
# ============================================================
def plot_3d_tx_ego(txid: int, hops: int = 2, max_nodes: int = 400):
    txid = int(txid)

    if txid not in G_full:
        raise ValueError(f"txId {txid} not found")

    ego = nx.ego_graph(G_full, txid, radius=hops)

    if ego.number_of_nodes() > max_nodes:
        nodes = list(ego.nodes())
        nodes.remove(txid)
        ranked = sorted(nodes, key=lambda n: ego.degree[n], reverse=True)
        ego = ego.subgraph([txid] + ranked[:max_nodes - 1])

    pos = nx.spring_layout(ego, dim=3, seed=42, k=0.38, iterations=80)

    nodes = list(ego.nodes())

    # ============================================================
    # NEW GREEN → YELLOW → RED COLORS
    # ============================================================
    risk_colors = {
        "High": "#ff0000",     # red
        "Medium": "#ffd000",   # yellow
        "Low": "#00cc44",      # green
        "Safe": "#5596ff"      # blue
    }

    # ============================================================
    # CATEGORY TRACES
    # ============================================================
    node_traces = []

    for category in ["High", "Medium", "Low", "Safe"]:

        cat_nodes = [n for n in nodes if bucket_map.get(n, "Safe") == category]
        if not cat_nodes:
            continue

        node_traces.append(
            go.Scatter3d(
                x=[pos[n][0] for n in cat_nodes],
                y=[pos[n][1] for n in cat_nodes],
                z=[pos[n][2] for n in cat_nodes],
                mode="markers",
                name=f"{category} Risk",
                marker=dict(
                    size=[min(32, max(10, ego.degree[n] * 1.8)) for n in cat_nodes],
                    color=risk_colors[category],
                    opacity=0.93,
                    line=dict(color="white", width=0.8),
                ),
                text=[
                    f"<b>txId:</b> {n}<br>"
                    f"<b>Risk:</b> {category}<br>"
                    f"<b>p(illicit):</b> {proba_map.get(n):.4f}<br>"
                    f"<b>Degree:</b> {ego.degree[n]}"
                    for n in cat_nodes
                ],
                hoverinfo="text"
            )
        )

    # ============================================================
    # EDGES
    # ============================================================
    edge_x, edge_y, edge_z = [], [], []
    for u, v in ego.edges():
        x0, y0, z0 = pos[u]; x1, y1, z1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_z += [z0, z1, None]

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode="lines",
        line=dict(width=1, color="rgba(255,255,255,0.12)"),
        hoverinfo="none",
        name="Edges",
        showlegend=False
    )

# ============================================================
# ROOT NODE — HOT PINK (#ff1493) + WHITE OUTLINE
# ============================================================
    sx, sy, sz = pos[txid]
    
    seed_trace = go.Scatter3d(
        x=[sx], y=[sy], z=[sz],
        mode="markers",
        name="ROOT Transaction",
        marker=dict(
            size=16,
            color="#ff1493",              # ⭐ HOT PINK ROOT
            symbol="diamond",
            line=dict(color="white", width=4),   # strong white outline
            opacity=1.0
        ),
        text=[f"<b>ROOT txId:</b> {txid}<br>"
              f"<b>p(illicit):</b> {proba_map.get(txid):.4f}"],
        hoverinfo="text",
    )
    
    # ============================================================
    # ROOT GLOW EFFECT (SOFT HOT PINK HALO)
    # ============================================================
    glow_trace = go.Scatter3d(
        x=[sx], y=[sy], z=[sz],
        mode="markers",
        marker=dict(
            size=45,
            color="rgba(255, 20, 147, 0.18)",  # soft hot-pink glow
            symbol="circle",
            opacity=0.18
        ),
        hoverinfo="none",
        showlegend=False
    )
    
    # ============================================================
    # ROOT LABEL
    # ============================================================
    seed_label = go.Scatter3d(
        x=[sx], y=[sy], z=[sz + 0.1],
        mode="text",
        text=[f"<b>ROOT<br>{txid}</b>"],
        textfont=dict(size=16, color="#ff1493"),   # label also hot pink
        hoverinfo="none",
        showlegend=False
    )

    # ============================================================
    # FIGURE BUILD
    # ============================================================
    fig = go.Figure(data=[edge_trace, glow_trace] + node_traces + [seed_trace, seed_label])

    fig.update_layout(
        title=f"<b>3D Transaction Ego Graph</b> (txId {txid})",
        title_font=dict(size=20, color="white"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        margin=dict(l=0, r=0, t=60, b=0),
        scene_camera=dict(eye=dict(x=1.4, y=1.4, z=1.1)),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.15)",
            borderwidth=1,
            font=dict(color="white")
        )
    )

    return fig
