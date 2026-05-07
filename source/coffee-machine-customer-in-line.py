def coffee_machine(coffee_type):
    coffee_cup = ""
    if coffee_type == '1':
        coffee_cup = "Espresso"
    elif coffee_type == '2':
        coffee_cup = "Latte"
    elif coffee_type == '3':
        coffee_cup = "Cappuccino"
    else:
        print("Invalid choice. Please select a valid option.")
    return coffee_cup

try:
    n = int(input("How many customers are in line? "))
except ValueError:
    print("Please enter a valid integer for the number of customers.")
    n = 0

if n <= 0:
    print("No more customers in the line.")
else:
    customers = []
    for i in range(n):
        name = input(f"Enter name of customer {i+1}: ").strip()
        customers.append(name or f"Customer{i+1}")

    for customer in customers:
        choice = input(f"{customer}, please select a coffee type (1: Espresso, 2: Latte, 3: Cappuccino): ")
        order = coffee_machine(choice)
        if order:
            print(f"{customer} ordered: {order}")
        else:
            print(f"{customer} did not place a valid order.")
    print("No more customers in the line.")