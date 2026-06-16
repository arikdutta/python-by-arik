import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

patient_name = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry"]

# Features: [age, bmi, blood_pressure_systolic, chronic_conditions, hospitalizations_per_year, smoker]
patient_data = [
    [25, 22.1, 110, 0, 0, 0],   # Alice  - young, healthy
    [30, 24.5, 118, 0, 0, 0],   # Bob    - young, healthy
    [45, 27.8, 130, 1, 1, 0],   # Carol  - moderate risk
    [50, 29.3, 138, 2, 2, 1],   # David  - moderate-high risk
    [62, 33.5, 150, 3, 4, 1],   # Eve    - high risk
    [68, 35.2, 165, 4, 6, 1],   # Frank  - high risk
    [55, 31.0, 145, 2, 3, 0],   # Grace  - moderate risk
    [72, 36.8, 175, 5, 8, 1],   # Henry  - very high risk
]


model = KMeans(n_clusters=3, random_state=42)
model.fit(patient_data)
labels = model.labels_

# Map cluster IDs to risk levels: higher average age+bmi+bp+conditions = higher risk
cluster_scores = []
for cluster_id in range(3):
    cluster_indices = np.where(labels == cluster_id)[0]
    avg_score = np.array(patient_data)[cluster_indices].mean(axis=0)
    # weighted risk score: chronic conditions and hospitalizations matter most
    risk_score = avg_score[3] * 3 + avg_score[4] * 2 + avg_score[0] * 0.5 + avg_score[1] * 0.5
    cluster_scores.append((cluster_id, risk_score))

cluster_scores.sort(key=lambda x: x[1])
risk_map = {
    cluster_scores[0][0]: "Low Risk",
    cluster_scores[1][0]: "Medium Risk",
    cluster_scores[2][0]: "High Risk",
}
risk_labels = [risk_map[label] for label in labels]

print("\nHealthcare Patient Risk Profile:")
print(f"{'Patient':<10} {'Age':>5} {'BMI':>6} {'BP':>5} {'Conditions':>11} {'Hospitalizations':>17} {'Smoker':>7}  Risk")
print("-" * 80)
for i, (name, risk) in enumerate(zip(patient_name, risk_labels)):
    age, bmi, bp, cond, hosp, smoke = patient_data[i]
    print(f"  {name:<8} {age:>5} {bmi:>6.1f} {bp:>5} {cond:>11} {hosp:>17} {'Yes' if smoke else 'No':>7}  -> {risk}")

colors = {"Low Risk": "green", "Medium Risk": "orange", "High Risk": "red"}
point_colors = [colors[r] for r in risk_labels]

ages  = [row[0] for row in patient_data]
bmis  = [row[1] for row in patient_data]

plt.figure(figsize=(8, 6))
plt.scatter(ages, bmis, c=point_colors, s=120, edgecolors="black", linewidths=0.7)

for i, name in enumerate(patient_name):
    plt.annotate(
        f"{name}\n({risk_labels[i]})",
        (ages[i], bmis[i]),
        textcoords="offset points",
        xytext=(6, 5),
        fontsize=8,
    )

plt.xlabel("Age")
plt.ylabel("BMI")
plt.title("Healthcare Patient Risk Segmentation")

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, label=r) for r, c in colors.items()]
plt.legend(handles=legend_elements, loc="upper left")

plt.tight_layout()
plt.show()
