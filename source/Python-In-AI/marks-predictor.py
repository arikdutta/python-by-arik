from sklearn.linear_model import LinearRegression
 
hours = [[1], [2], [3], [4],[5], [6], [7], [8]]
 
marks = [20, 25, 30, 36, 41, 58, 64, 88]
 
model = LinearRegression()
 
model.fit(hours, marks)

input_hours =float(input("Enter hours studied: "))
prediction = model.predict([[input_hours]])
 
print("Predicted marks: ",prediction)
