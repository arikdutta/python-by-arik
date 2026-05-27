import pandas as pd

df = pd.read_csv("C:\\Users\\dutta\\python-by-arik\\source\\data-.csv")
print(df.head())
print(df.info())
print(df.isnull().sum())
df = df.fillna(0)
print(df.head())
df['total'] = df['a'] + df['b']
print(df.head())
print(df.duplicated())
df["sales"] = df["sales"].fillna(0)