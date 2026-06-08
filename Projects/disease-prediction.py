from sklearn.tree import DecisionTreeClassifier
 
symptoms = [
 
    [1,1,1],
    [1,1,0],
    [1,0,1],
 
    [0,0,0],
    [0,1,0],
    [0,0,1]
 
]
 
result = [
 
    "Disease",
    "Disease",
    "Disease",
 
    "No Disease",
    "No Disease",
    "No Disease"
 
]
 
model = DecisionTreeClassifier()
 
model.fit(symptoms,result)
 
fever = int(input("Fever? (1 Yes / 0 No): "))
 
cough = int(input("Cough? (1 Yes / 0 No): "))
 
pain = int(input("Body Pain? (1 Yes / 0 No): "))
 
prediction = model.predict([[fever,cough,pain]])
 
print("Prediction:",prediction[0])