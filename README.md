💰 Illicit Transaction Detection in Cryptocurrency Networks Using Graph Analytics
📌 Overview

This project develops an intelligent illicit cryptocurrency transaction detection system using Machine Learning and Graph Analytics. The system analyzes Bitcoin transaction behaviour and network structures to classify transactions as licit (legitimate) or illicit (suspicious or criminal).

The model is trained on the Elliptic Bitcoin Dataset, which contains over 200,000 real Bitcoin transactions and their relationships within the blockchain network. By combining feature-based machine learning, graph-based analytics, and semi-supervised learning, the system detects suspicious activity patterns similar to those investigated in banking Anti-Money Laundering (AML) systems.

The final system can assist financial institutions, regulators, and compliance teams in identifying risky cryptocurrency transactions and monitoring blockchain-based financial behaviour. 

Banking Report

🗂️ Dataset

This project uses the Elliptic Bitcoin Transaction Dataset, a widely used dataset for blockchain illicit activity research.

Property	Details
Total Transactions	203,769
Graph Edges	234,355
Features per Transaction	166
Labels	Licit, Illicit, Unknown
Illicit Transactions	~2%
Licit Transactions	~21%
Unknown	~77%

The dataset is composed of three main files:

1️⃣ Transaction Features

elliptic_txs_features.csv

Contains 166 features describing each transaction including:

Number of inputs / outputs

Transaction amount

Transaction fees

Temporal information

Aggregated graph-based statistics

These features capture transaction behaviour and financial patterns.

2️⃣ Transaction Labels

elliptic_txs_classes.csv

Label	Meaning
1	Illicit
2	Licit
Unknown	Unlabelled

This file provides the ground truth classification used for supervised learning.

3️⃣ Transaction Graph

elliptic_txs_edgelist.csv

Represents the Bitcoin transaction network.

Transaction A → Transaction B

Meaning B spends the output of A, forming a directed graph of fund flow.

This graph structure allows detection of money laundering patterns and suspicious transaction chains. 

Banking Report

🏗️ System Architecture
Bitcoin Transaction Dataset
        │
        ▼
Data Cleaning & Preprocessing
        │
        ▼
Feature Engineering
(166 Behavioral + Graph Features)
        │
        ▼
Label Handling
(Labelled + Unlabelled Data)
        │
        ▼
Supervised Model
(LightGBM)
        │
        ▼
Semi-Supervised Learning
(Pseudo Labeling)
        │
        ▼
Graph Analysis
(NetworkX Metrics)
        │
        ▼
Risk Prediction
(Safe / Low / Medium / High)
        │
        ▼
TIGER Visualization
(Graph Risk Investigation)
🧠 Models & Techniques Used
Machine Learning Model
Model	Purpose
LightGBM	Main classifier for detecting illicit transactions

LightGBM was selected because it:

Handles large-scale datasets efficiently

Works well with imbalanced classes

Captures complex nonlinear relationships

Graph-Based Analysis

The project also incorporates graph analytics to analyze the Bitcoin transaction network.

Graph metrics used:

Metric	Purpose
Degree Centrality	Detect high transaction hubs
Betweenness Centrality	Identify bridge transactions
Clustering Coefficient	Detect suspicious clusters
Community Detection	Identify transaction networks

Graph analysis helps detect money laundering chains and coordinated transaction networks.

Semi-Supervised Learning

Because 77% of transactions are unlabeled, the project applies Pseudo-Labeling.

Workflow:

Train initial model on labeled data

Predict labels for unlabeled data

Select high-confidence predictions

Add them back into the training dataset

Retrain final model

This allows the model to learn hidden transaction patterns across the network. 

Banking Report

📊 Results
LightGBM Model Performance (Validation)
Metric	Licit	Illicit
Precision	0.9949	0.9332
Recall	0.9926	0.9527
F1 Score	0.9937	0.9428
Overall Accuracy
98.87%

These results show strong detection capability despite extreme class imbalance.

Training Performance
Metric	Score
Accuracy	99.59%
Macro F1 Score	0.9886
AUC	~0.999

This indicates the model effectively learns patterns of illicit behaviour.

Risk Distribution
Risk Level	Count
Safe	183,646
Low	2,296
Medium	1,580
High	16,247

Most transactions are safe, but the system successfully isolates a small high-risk group for investigation.

🔍 TIGER Graph Analysis

The project includes a TIGER-style network visualization system for AML investigation.

Features:

2D & 3D transaction graph

Risk-based node colouring

Transaction relationship tracing

Cluster detection

Investigators can:

Track suspicious fund flows

Identify illicit clusters

Investigate laundering patterns visually.

⚙️ Methodology

The project follows the following pipeline:

1️⃣ Data Ingestion

Load and merge:

Transaction features

Labels

Graph edges

2️⃣ Feature Engineering

Key engineered features include:

Transaction ratios

Fee-to-amount relationships

Graph neighbourhood statistics

Temporal behaviour indicators

3️⃣ Model Training

Train LightGBM classifier on labelled transactions.

4️⃣ Semi-Supervised Learning

Use pseudo-labeling to incorporate unlabelled data.

5️⃣ Graph Analytics

Build transaction network using NetworkX.

Calculate:

Degree

Centrality

Clustering

6️⃣ Risk Scoring

Convert probabilities into risk categories:

Safe
Low Risk
Medium Risk
High Risk
7️⃣ Visualization

Use TIGER framework to display transaction network.

🛠️ Tech Stack
Programming

Python

Machine Learning

LightGBM

Scikit-learn

Graph Analytics

NetworkX

Data Processing

Pandas

NumPy

Visualization

Matplotlib

Seaborn

Graph Visualization (TIGER)

Deployment

Streamlit

HuggingFace

🌐 Deployment

The system is deployed as an interactive AML analytics tool.

Users can:

Upload transaction data

Predict illicit probability

Visualize transaction networks

Investigate suspicious clusters

Deployment platforms:

Streamlit Dashboard

HuggingFace Model Hosting 

Banking Report
