from sklearn.linear_model import LinearRegression
 
X = [[2], [4], [6], [8]]
 
y = [40, 55, 70, 85]
 
model = LinearRegression()
 
model.fit(X, y)
 
prediction = model.predict([[15]])
 
print(prediction)