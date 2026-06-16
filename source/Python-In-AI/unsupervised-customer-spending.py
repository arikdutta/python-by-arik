from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

customer_name = ["A", "B", "C", "D", "E", "F"]
Age = [20, 22,24, 50, 55, 60]

spending = [
 
[5000],
[6000],
[25000],
[30000],
[55000],
[60000]
 
]

model = KMeans(n_clusters = 2, random_state = 42)
model.fit(spending)
labels = model.labels_
print(labels)

plt.scatter(Age, spending, c=labels)
plt.xlabel("Age")
plt.ylabel("Spending")
plt.title("Customer Segmentation")
plt.show()