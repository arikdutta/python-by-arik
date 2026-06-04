import pandas as pd
from sklearn.ensemble import IsolationForest

df = pd.read_csv("transactions.csv")
model = IsolationForest(contamination=0.01)
model.fit(df[['amount','merchant_id','customer_id']])

df['fraud_score'] = model.decision_function(df[['amount','merchant_id','customer_id']])
df['is_fraud'] = model.predict(df[['amount','merchant_id','customer_id']])
print(df[df['is_fraud'] == -1])