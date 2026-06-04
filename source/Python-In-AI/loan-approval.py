from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression

# [annual salary, monthly expenses, loan amount requested, credit score (300-850), employment years]
loan_data = [
    [25000,  1200, 5000,  580, 1],
    [30000,  1500, 8000,  610, 2],
    [35000,  1800, 10000, 640, 3],
    [40000,  2000, 12000, 660, 4],
    [45000,  2200, 15000, 680, 5],
    [50000,  2500, 20000, 700, 6],
    [55000,  2700, 25000, 720, 7],
    [60000,  3000, 30000, 740, 8],
    [70000,  3500, 40000, 760, 9],
    [80000,  4000, 50000, 780, 10],
    [90000,  4500, 60000, 800, 12],
    [100000, 5000, 70000, 820, 15],
    [20000,  1800, 15000, 550, 1],
    [28000,  2500, 20000, 530, 2],
    [32000,  3000, 25000, 510, 1],
    [22000,  2000, 18000, 480, 0],
    [15000,  1500, 12000, 450, 0],
    [18000,  1700, 10000, 500, 1],
    [45000,  4000, 40000, 580, 3],
    [38000,  3500, 35000, 560, 2],
]

labels = [
    "Rejected", "Rejected", "Approved", "Approved", "Approved",
    "Approved", "Approved", "Approved", "Approved", "Approved",
    "Approved", "Approved", "Rejected", "Rejected", "Rejected",
    "Rejected", "Rejected", "Rejected", "Rejected", "Rejected",
]

# Encode labels as 1 (Approved) / 0 (Rejected) for linear regression
numeric_labels = [1 if l == "Approved" else 0 for l in labels]

decision_tree = DecisionTreeClassifier()
decision_tree.fit(loan_data, labels)

linear_model = LinearRegression()
linear_model.fit(loan_data, numeric_labels)

print("=== Bank Loan Approval System ===\n")
annual_salary    = float(input("Annual salary ($): "))
monthly_expenses = float(input("Monthly expenses ($): "))
loan_amount      = float(input("Loan amount requested ($): "))
credit_score     = float(input("Credit score: "))
employment_years = float(input("Years of employment: "))

applicant = [[annual_salary, monthly_expenses, loan_amount, credit_score, employment_years]]

dt_decision = decision_tree.predict(applicant)[0]

lr_score = linear_model.predict(applicant)[0]
lr_score = max(0.0, min(1.0, lr_score))  # clamp to [0, 1]
lr_decision = "Approved" if lr_score >= 0.5 else "Rejected"

print(f"\n--- Decision Tree        : {dt_decision}")
print(f"--- Linear Regression    : {lr_decision} (approval score: {lr_score:.2f})")
