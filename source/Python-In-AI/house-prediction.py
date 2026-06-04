from sklearn.tree import DecisionTreeClassifier

# [house size in sqft, price in EUR]
house_data = [
    [500, 74000], [600, 88000], [750, 111000], [800, 139000],
    [900, 167000], [1000, 185000], [1100, 231000], [1200, 250000],
    [1300, 287000], [1500, 370000], [1600, 417000], [1800, 509000]
]

fit_unfit = ["Fit", "Fit", "Fit", "Fit", "Fit", "Fit", "Unfit", "Fit", "Unfit", "Unfit", "Unfit", "Unfit"]

model = DecisionTreeClassifier()

model.fit(house_data, fit_unfit)

input_size = float(input("Enter house size (sqft): "))
input_price = float(input("Enter house price (EUR): "))
prediction = model.predict([[input_size, input_price]])

print("Predicted fit/unfit to buy based on size and price:", prediction[0])
