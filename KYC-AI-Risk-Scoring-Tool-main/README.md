# KYC AI Risk Scoring Tool 🔍

## Project Overview
This project automates the KYC (Know Your Customer) customer risk assessment process using Artificial Intelligence and Machine Learning. It replicates the manual work that a KYC analyst performs every day — analysing customer profiles and classifying them as Low, Medium or High risk.

## Business Problem
In real banking and financial institutions, KYC analysts manually review hundreds of customer profiles to assess risk. This process is time-consuming and inconsistent. This tool uses AI to automate and standardise that process.

## What This Tool Does
- Analyses customer data including country, occupation, PEP status, income and transactions
- Automatically classifies customers as Low, Medium or High risk
- Flags Politically Exposed Persons (PEPs) for Enhanced Due Diligence (EDD)
- Compares two AI models — Random Forest and Logistic Regression

## Models Used
| Model | Accuracy |
|---|---|
| Random Forest | 83.33% |
| Logistic Regression | 100% (overfitting) |

Random Forest is the recommended model as it generalises better to new unseen customers.

## Key Features
- Customer Risk Distribution Chart
- High Risk Countries Analysis
- PEP Customer Detection
- AI Risk Prediction on New Customers
- Model Comparison and Evaluation

## Technologies Used
- Python
- Pandas
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook

## Files
- `KYC_Risk_Scoring.ipynb` — Main project notebook
- `KYC_Customer_Data.xlsx` — Mock customer dataset

## Author
Reshma | MSc Artificial Intelligence | KYC & AML Compliance
