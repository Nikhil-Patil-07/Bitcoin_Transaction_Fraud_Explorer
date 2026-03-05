# ₿ Illicit Transaction Detection in Cryptocurrency Networks Using Graph Analytics

### Machine Learning & Graph Analytics for Blockchain Anti-Money Laundering (AML)

---

## 📌 Overview
---

This project develops an **AI-driven illicit cryptocurrency transaction detection system** designed to identify suspicious activity within **Bitcoin transaction networks**.

The system analyzes **transaction behaviour, temporal patterns, and network structures** using **Machine Learning and Graph Analytics** to classify transactions as:

- **Licit (Legitimate)**
- **Illicit (Suspicious or Criminal)**

The model is trained on the **Elliptic Bitcoin Dataset**, which contains more than **200,000 real-world Bitcoin transactions** and their relationships within the blockchain.

By combining:

- **Feature-based Machine Learning**
- **Graph Network Analysis**
- **Semi-Supervised Learning**

the system detects patterns similar to those investigated in **banking Anti-Money Laundering (AML) systems**.

---

## 🎯 Key Features
---

- 🔍 **Illicit transaction detection** using machine learning models  
- 🌐 **Graph network analysis of blockchain transactions**  
- 🧠 **Semi-supervised learning with pseudo-labeling**  
- 📊 **Risk scoring system** (Safe / Low / Medium / High)  
- 🔗 **Graph visualization for AML investigation**

---

## 🗂️ Dataset
---

This project uses the **Elliptic Bitcoin Transaction Dataset**, a benchmark dataset widely used in cryptocurrency fraud detection research.

| Property | Details |
|---|---|
| Total Transactions | 203,769 |
| Graph Edges | 234,355 |
| Features per Transaction | 166 |
| Labels | Licit / Illicit / Unknown |
| Illicit Transactions | ~2% |
| Licit Transactions | ~21% |
| Unknown Transactions | ~77% |

---

### 1️⃣ Transaction Features

`elliptic_txs_features.csv`

Contains **166 features** describing each transaction including:

- Number of inputs and outputs  
- Transaction amount  
- Transaction fees  
- Temporal information  
- Aggregated graph-based statistics  

These features capture **transaction behaviour and financial patterns**.

---

### 2️⃣ Transaction Labels

`elliptic_txs_classes.csv`

| Label | Meaning |
|---|---|
| 1 | Illicit |
| 2 | Licit |
| Unknown | Unlabeled |

This file provides the **ground truth classification used for supervised learning**.

---

### 3️⃣ Transaction Graph

`elliptic_txs_edgelist.csv`

Represents the **Bitcoin transaction network**.

---

---
### Transaction A → Transaction B

Meaning **transaction B spends the output of transaction A**, forming a **directed graph of fund flow**.

This graph structure allows detection of:

- Money laundering patterns  
- Suspicious transaction chains  
- Network-based criminal behaviour  

---

## 🏗️ System Architecture
---
<img width="347" height="597" alt="image" src="https://github.com/user-attachments/assets/9ac0c976-5a92-4bb3-b845-d1782a7ff0f1" />


## 🧠 Models & Techniques Used
---

### Machine Learning Model

| Model | Purpose |
|---|---|
| LightGBM | Main classifier for detecting illicit transactions |

LightGBM was selected because it:

- Handles **large-scale datasets efficiently**
- Works well with **imbalanced data**
- Captures **complex nonlinear relationships**

---

### Graph-Based Analysis

The project incorporates **graph analytics** to analyze the Bitcoin transaction network.

| Metric | Purpose |
|---|---|
| Degree Centrality | Detect high transaction hubs |
| Betweenness Centrality | Identify bridge transactions |
| Clustering Coefficient | Detect suspicious clusters |
| Community Detection | Identify transaction networks |

Graph analysis helps detect **money laundering chains and coordinated transaction networks**.

---

### Semi-Supervised Learning

Because **77% of transactions are unlabeled**, the project applies **Pseudo-Labeling**.

Workflow:

1. Train initial model on labeled data  
2. Predict labels for unlabeled data  
3. Select high-confidence predictions  
4. Add them back into the training dataset  
5. Retrain the final model  

This allows the model to learn **hidden transaction patterns across the network**.

---

## 📊 Results
---

### LightGBM Model Performance (Validation)

| Metric | Licit | Illicit |
|---|---|---|
| Precision | 0.9949 | 0.9332 |
| Recall | 0.9926 | 0.9527 |
| F1 Score | 0.9937 | 0.9428 |

---

### Overall Accuracy: - 98.87%

These results show strong detection capability **despite extreme class imbalance**.

---

### Training Performance

| Metric | Score |
|---|---|
| Accuracy | 99.59% |
| Macro F1 Score | 0.9886 |
| AUC | ~0.999 |

This indicates the model effectively learns **patterns of illicit behaviour**.

---

## 📈 Risk Distribution
---

| Risk Level | Count |
|---|---|
| Safe | 183,646 |
| Low | 2,296 |
| Medium | 1,580 |
| High | 16,247 |

Most transactions are **safe**, but the system successfully isolates a **small high-risk group for investigation**.

---

## 🛠️ Tech Stack
---

**Programming**

- Python

**Machine Learning**

- LightGBM  
- Scikit-learn  

**Graph Analytics**

- NetworkX  

**Data Processing**

- Pandas  
- NumPy  

**Visualization**

- Matplotlib  
- Seaborn  

**Deployment**

- Streamlit  
- HuggingFace  

---

## 🌐 Deployment
---

The system is deployed as an **interactive AML analytics tool**.

Users can:

- Upload transaction data  
- Predict illicit probability  
- Visualize transaction networks  
- Investigate suspicious clusters  

Deployment platforms:

- **Streamlit Dashboard**
- **HuggingFace Model Hosting**

---
🔗 Live Demo: https://huggingface.co/spaces/Nikhil0702/Bitcoin_Transaction_Fraud_Explorer

### 📝NOTE: -If it is sleeping just click on the "Restart the Space"

