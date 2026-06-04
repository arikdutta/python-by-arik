# Importing required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading the Excel file into a pandas dataframe
df = pd.read_excel("KYC_Customer_Data.xlsx")
df.head(10)

# Checking total number of customers
print("Total Customers:", len(df))
# Checking all column names
print("Columns:", df.columns.tolist())
# Checking how many customers fall into each risk category
print("\nRisk Level Breakdown:")
print(df["Risk_Level"].value_counts())

# Chart 1 - Overall Risk Level Distribution
colors = ["green", "orange", "red"]
df["Risk_Level"].value_counts().plot(kind="bar", color=colors)
plt.title("Customer Risk Level Distribution")
plt.xlabel("Risk Level")
plt.ylabel("Number of Customers")
plt.xticks(rotation=0)
plt.show()

# Chart 2 - High Risk Customers by Country
# This shows which countries have the most high risk customers
high_risk = df[df["Risk_Level"] == "High"]
high_risk["Country"].value_counts().plot(kind="bar", color="red")
plt.title("High Risk Customers by Country")
plt.xlabel("Country")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)
plt.show()