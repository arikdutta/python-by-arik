from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# [age, prior_admissions, num_diagnoses, num_medications, days_in_hospital, er_visits_last_year, has_chronic_condition, discharged_to_home]
patient_data = [
    [72, 3, 8, 12, 7,  3, 1, 0],
    [65, 2, 6, 10, 5,  2, 1, 1],
    [80, 5, 9, 14, 10, 4, 1, 0],
    [55, 1, 4,  7, 3,  1, 0, 1],
    [78, 4, 7, 11, 8,  3, 1, 0],
    [60, 2, 5,  9, 4,  1, 1, 1],
    [45, 0, 2,  3, 2,  0, 0, 1],
    [70, 3, 8, 13, 9,  2, 1, 0],
    [58, 1, 3,  6, 3,  0, 0, 1],
    [83, 6, 10, 15, 12, 5, 1, 0],
    [50, 0, 2,  4, 2,  0, 0, 1],
    [75, 4, 9, 12, 8,  3, 1, 1],
    [66, 2, 6,  8, 5,  2, 1, 1],
    [88, 7, 11, 16, 14, 6, 1, 0],
    [40, 0, 1,  2, 1,  0, 0, 1],
    [73, 3, 7, 10, 7,  2, 1, 0],
    [52, 1, 3,  5, 2,  1, 0, 1],
    [79, 5, 8, 13, 9,  4, 1, 0],
    [62, 2, 5,  7, 4,  1, 1, 1],
    [47, 0, 2,  3, 2,  0, 0, 1],
    [85, 6, 10, 14, 11, 5, 1, 0],
    [57, 1, 4,  6, 3,  1, 0, 1],
    [71, 3, 7, 11, 6,  2, 1, 1],
    [68, 2, 5,  9, 5,  1, 1, 1],
    [76, 4, 8, 12, 8,  3, 1, 0],
    [44, 0, 1,  2, 1,  0, 0, 1],
    [82, 5, 9, 13, 10, 4, 1, 0],
    [54, 1, 3,  5, 3,  0, 0, 1],
    [69, 3, 6, 10, 6,  2, 1, 0],
    [61, 1, 4,  7, 4,  1, 1, 1],
]

labels = [
    "Readmitted",     "Not Readmitted", "Readmitted",     "Not Readmitted", "Readmitted",
    "Not Readmitted", "Not Readmitted", "Readmitted",     "Not Readmitted", "Readmitted",
    "Not Readmitted", "Readmitted",     "Not Readmitted", "Readmitted",     "Not Readmitted",
    "Readmitted",     "Not Readmitted", "Readmitted",     "Not Readmitted", "Not Readmitted",
    "Readmitted",     "Not Readmitted", "Readmitted",     "Not Readmitted", "Readmitted",
    "Not Readmitted", "Readmitted",     "Not Readmitted", "Readmitted",     "Not Readmitted",
]

X_train, X_test, y_train, y_test = train_test_split(
    patient_data,
    labels,
    test_size=0.2,
    random_state=42
)

decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, y_train)


y_pred = decision_tree.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
# Calculate accuracy

print("Testing:", X_test)
print(f"\n--- Decision Tree        : {y_pred}")
print(f"Decision Tree Accuracy: {accuracy * 100:.1f}%\n")
