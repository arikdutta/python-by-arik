import numpy as np

employees = np.array([
    "Employee 1", "Employee 2", "Employee 3", "Employee 4", "Employee 5",
    "Employee 6", "Employee 7", "Employee 8", "Employee 9", "Employee 10"
])

salaries = np.array([50000, 62000, 45000, 71000, 58000, 83000, 39000, 67000, 54000, 76000], dtype=float)

increments = np.array([10, 8, 12, 5, 15, 7, 20, 9, 11, 6], dtype=float)  # percentage

# Calculate increases and updated salaries
increases = salaries * increments / 100
new_salaries = salaries + increases

print("=" * 65)
print(f"{'SALARY INCREMENT SYSTEM':^65}")
print("=" * 65)
print(f"{'Employee':<12} {'Old Salary':>12} {'Increment':>10} {'New Salary':>12} {'Increase':>10}")
print("-" * 65)

for i in range(len(employees)):
    print(f"{employees[i]:<12} {salaries[i]:>12,.2f} {increments[i]:>9.0f}% {new_salaries[i]:>12,.2f} {increases[i]:>10,.2f}")

print("=" * 65)

highest_idx = np.argmax(new_salaries)
lowest_idx  = np.argmin(new_salaries)
avg_increase = np.mean(increases)
total_old    = np.sum(salaries)
total_new    = np.sum(new_salaries)

print(f"\n{'SUMMARY':^65}")
print("-" * 65)
print(f"  Highest Salary : {employees[highest_idx]:<12} => ${new_salaries[highest_idx]:,.2f}")
print(f"  Lowest Salary  : {employees[lowest_idx]:<12} => ${new_salaries[lowest_idx]:,.2f}")
print(f"  Total Old Cost : ${total_old:,.2f}")
print(f"  Total New Cost : ${total_new:,.2f}")
print(f"  Total Increase : ${total_new - total_old:,.2f}")
print(f"  Avg Increase   : ${avg_increase:,.2f} per employee")
print("=" * 65)
