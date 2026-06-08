from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
 
house_data = [
[500, 74000], [600, 88000], [750, 111000], [800, 139000],
[900, 167000], [1000, 185000], [1100, 231000], [1200, 250000],
[1300, 287000], [1500, 370000], [1600, 417000], [1800, 509000]
]
 
fit_unfit = [
"Fit", "Fit", "Fit", "Fit", "Fit", "Fit",
"Unfit", "Fit", "Unfit", "Unfit", "Unfit", "Unfit"
]
 
# Split data
 
X_train, X_test, y_train, y_test = train_test_split(
    house_data,
    fit_unfit,
    test_size=0.2,
    random_state=42
)
 
# Create model
 
model = DecisionTreeClassifier()
 
# Train model
 
model.fit(X_train, y_train)
 
# Predict test data
 
y_pred = model.predict(X_test)
 
# Calculate accuracy

print("Testing:", X_test)
print(f"\n--- Decision Tree        : {y_pred}")
accuracy = accuracy_score(y_test, y_pred)
 
print("Accuracy:", accuracy * 100, "%")