import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

customer_name = ["A", "B", "C", "D", "E", "F"]
income = [50000, 60000, 70000, 50000, 55000, 60000]
emi = [

[0],
[1000],

[90000],
[100000],

[40000],
[50000]

]

model = KMeans(n_clusters = 3, random_state = 42)
model.fit(emi)
labels = model.labels_

# Map cluster IDs to risk levels based on EMI center values (higher EMI = higher risk)
centers = model.cluster_centers_.flatten()
sorted_cluster_ids = np.argsort(centers)  # ascending EMI order
risk_map = {sorted_cluster_ids[0]: "Low Risk", sorted_cluster_ids[1]: "Medium Risk", sorted_cluster_ids[2]: "High Risk"}
risk_labels = [risk_map[label] for label in labels]

print("\nCustomer Risk Profile:")
for name, risk in zip(customer_name, risk_labels):
    print(f"  Customer {name}: {risk}")

emi_flat = [e[0] for e in emi]
colors = {"Low Risk": "green", "Medium Risk": "orange", "High Risk": "red"}
point_colors = [colors[r] for r in risk_labels]

# plt.scatter(income, emi_flat, c=point_colors)
# for i, name in enumerate(customer_name):
#     plt.annotate(f"{name}\n({risk_labels[i]})", (income[i], emi_flat[i]), textcoords="offset points", xytext=(5, 5), fontsize=8)
plt.xlabel("Income")
plt.ylabel("EMI")
plt.title("Customer Risk Segmentation")
plt.show()