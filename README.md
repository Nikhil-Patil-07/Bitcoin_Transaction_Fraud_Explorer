₿ Illicit Transaction Detection in Cryptocurrency Networks
Machine Learning & Graph Analytics for Blockchain Anti-Money Laundering (AML)

M.Sc. Thesis Project — Symbiosis Institute of Geoinformatics, Symbiosis International (Deemed University)
Author: Nikhil Anil Patil | Batch: 2024–2026 | PRN: 24070243038
Project Title: Illicit Transaction Detection in Cryptocurrency Networks Using Graph Analytics

📌 Overview

This project develops an AI-driven illicit cryptocurrency transaction detection system designed to identify suspicious activity within Bitcoin transaction networks.

The system analyzes transaction behaviour, temporal patterns, and network structures using Machine Learning and Graph Analytics to classify transactions as:

Licit (Legitimate)

Illicit (Suspicious or Criminal)

The model is trained on the Elliptic Bitcoin Dataset, which contains more than 200,000 real-world Bitcoin transactions and their relationships within the blockchain.

By combining:

Feature-based Machine Learning

Graph Network Analysis

Semi-Supervised Learning

the system detects patterns similar to those investigated in Anti-Money Laundering (AML) systems used by banks and financial institutions.

The system can assist:

Banks

Financial regulators

Cryptocurrency exchanges

Compliance teams

in identifying risky blockchain activity and monitoring crypto-linked financial behaviour.

🎯 Key Features

🔎 Illicit transaction detection using advanced ML models

📊 Graph analytics on Bitcoin transaction networks

🧠 Semi-supervised learning to leverage unlabeled data

🌐 Risk scoring system (Safe / Low / Medium / High)

📉 Class imbalance handling in financial crime datasets

🧩 Interactive graph visualization (TIGER analysis)

🚀 Deployable AML analytics dashboard

🗂️ Dataset

This project uses the Elliptic Bitcoin Transaction Dataset, a widely used benchmark dataset for cryptocurrency illicit activity detection.

Property	Details
Total Transactions	203,769
Graph Edges	234,355
Features per Transaction	166
Labels	Licit / Illicit / Unknown
Illicit Transactions	~2%
Licit Transactions	~21%
Unknown Transactions	~77%

The dataset mirrors real-world blockchain environments, where most transactions are unlabeled.

📦 Dataset Structure

The dataset consists of three primary files.

1️⃣ Transaction Features

elliptic_txs_features.csv

Contains 166 behavioural and structural features describing each transaction, including:

Number of inputs and outputs

Transaction amount

Transaction fees

Temporal information

Aggregated graph statistics

These features help capture transaction behaviour and financial patterns.

2️⃣ Transaction Labels

elliptic_txs_classes.csv

Label	Meaning
1	Illicit
2	Licit
Unknown	Unlabeled

This file provides the ground truth classification used for supervised learning.

3️⃣ Transaction Graph

elliptic_txs_edgelist.csv

Defines relationships between transactions.

Transaction A → Transaction B

Meaning:

Transaction B spends the output of Transaction A

This creates a directed graph of Bitcoin fund flow, enabling detection of:

Money laundering chains

Suspicious transaction clusters

Network-based criminal activity.

🏗️ System Architecture

The system follows a multi-stage AML analytics pipeline.

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
(LightGBM Classifier)
        │
        ▼
Semi-Supervised Learning
(Pseudo Labeling)
        │
        ▼
Graph Analytics
(NetworkX Metrics)
        │
        ▼
Risk Prediction
(Safe / Low / Med
