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

enter_choice = input("Please select a coffee type (1: Espresso, 2: Latte, 3: Cappuccino): ")
result = coffee_machine(enter_choice)
print(result)
