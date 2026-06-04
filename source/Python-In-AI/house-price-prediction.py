from sklearn.linear_model import LinearRegression
 
house_size = [
 
[500],
[800],
[1000],
[1200],
[1500]
]
 
price = [
 
20,
35,
50,
60,
75
]
 
model = LinearRegression()
 
model.fit(house_size, price)

input =float(input("Enter house size: "))
prediction = model.predict([[input]])
 
print("Predicted price: ",str(prediction[0]) + " lakhs")
