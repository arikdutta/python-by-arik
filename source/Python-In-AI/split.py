from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X = [[1],[2],[3],[4],[5],[6],[7],[8]]
 
y = [10,20,30,40,50,60,70,80]
 
X_train, X_test, y_train, y_test = train_test_split(
 
    X,
    y,
    test_size=0.2,
    random_state=42
 
)
 
print("Training:", X_train)
 
print("Testing:", X_test)

 
actual = [
 
    "Pass",
    "Pass",
    "Fail",
    "Fail"
 
]
 
predicted = [
 
    "Pass",
    "Pass",
    "Pass",
    "Fail"
 
]
 
accuracy = accuracy_score(
 
    actual,
    predicted
 
)
 
print(accuracy)