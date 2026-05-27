import pandas as pd

df = pd.read_csv(r"C:\Users\dutta\python-by-arik\source\data-.csv")
print(df)
df["sales"] = df["sales"].fillna(0)
print(df)
df["name"] = df["name"].fillna("Unknown")
df = df.rename(columns={"name":"New name"})
print(df)
sales = df[df['sales'] > 100]
print(sales)