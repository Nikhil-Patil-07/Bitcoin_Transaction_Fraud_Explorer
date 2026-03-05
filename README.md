
---

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

### Overall Accuracy
