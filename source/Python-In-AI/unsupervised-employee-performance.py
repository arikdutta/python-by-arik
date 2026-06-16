import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

employee_name = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry"]

# Features: [performance_score, hours_worked_per_week, projects_completed, training_hours, peer_review_score, absentee_days]
employee_data = [
    [92, 48, 12, 40, 90, 1],   # Alice  - high performer
    [88, 45, 10, 35, 85, 2],   # Bob    - high performer
    [74, 42, 7,  20, 72, 4],   # Carol  - moderate performer
    [70, 40, 6,  15, 68, 5],   # David  - moderate performer
    [55, 38, 4,  10, 60, 8],   # Eve    - low performer
    [50, 35, 3,  5,  55, 10],  # Frank  - low performer
    [78, 43, 8,  25, 75, 3],   # Grace  - moderate performer
    [45, 33, 2,  3,  50, 12],  # Henry  - low performer
]

model = KMeans(n_clusters=3, random_state=42)
model.fit(employee_data)
labels = model.labels_

# Map cluster IDs to performance levels: higher score + projects + training = higher performance
cluster_scores = []
for cluster_id in range(3):
    cluster_indices = np.where(labels == cluster_id)[0]
    avg_score = np.array(employee_data)[cluster_indices].mean(axis=0)
    # weighted performance score: performance score and projects completed matter most
    perf_score = avg_score[0] * 2 + avg_score[2] * 3 + avg_score[4] * 1.5 - avg_score[5] * 2
    cluster_scores.append((cluster_id, perf_score))

cluster_scores.sort(key=lambda x: x[1])
perf_map = {
    cluster_scores[0][0]: "Low Performer",
    cluster_scores[1][0]: "Average Performer",
    cluster_scores[2][0]: "High Performer",
}
perf_labels = [perf_map[label] for label in labels]

print("\nEmployee Performance Profile:")
print(f"{'Employee':<10} {'Score':>6} {'Hours':>6} {'Projects':>9} {'Training':>9} {'Peer Review':>12} {'Absent':>7}  Level")
print("-" * 90)
for i, (name, level) in enumerate(zip(employee_name, perf_labels)):
    score, hours, projects, training, peer, absent = employee_data[i]
    print(f"  {name:<8} {score:>6} {hours:>6} {projects:>9} {training:>9} {peer:>12} {absent:>7}  -> {level}")

colors = {"Low Performer": "red", "Average Performer": "orange", "High Performer": "green"}
point_colors = [colors[p] for p in perf_labels]

scores    = [row[0] for row in employee_data]
projects  = [row[2] for row in employee_data]

plt.figure(figsize=(8, 6))
plt.scatter(scores, projects, c=point_colors, s=120, edgecolors="black", linewidths=0.7)

for i, name in enumerate(employee_name):
    plt.annotate(
        f"{name}\n({perf_labels[i]})",
        (scores[i], projects[i]),
        textcoords="offset points",
        xytext=(6, 5),
        fontsize=8,
    )

plt.xlabel("Performance Score")
plt.ylabel("Projects Completed")
plt.title("Employee Performance Segmentation")

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, label=p) for p, c in colors.items()]
plt.legend(handles=legend_elements, loc="upper left")

plt.tight_layout()
plt.show()
