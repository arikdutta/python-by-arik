from sklearn.tree import DecisionTreeClassifier
 
years_salary = [[1,2000], [2,6000], [3,7000], [4,9500],[5,10000], [6,12500], [7,15000], [8,20000]]

fit_unfit = ["Fit", "Unfit", "Fit", "Fit", "Unfit", "Fit", "Fit", "Fit"]

model = DecisionTreeClassifier()
 
model.fit(years_salary, fit_unfit)


input_years = float(input("Enter years of experience: "))
input_salary = float(input("Enter salary: "))
prediction = model.predict([[input_years, input_salary]])
 
print("Predicted fit/unfit on basis of year and salary: ", prediction[0])