import time


def ask_choice(prompt, options):

    print(prompt)

    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")

    while True:

        choice = input("Enter your choice: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]

        print(f"  Invalid choice. Please enter a number between 1 and {len(options)}.")


def make_coffee(coffee_type, beans, milk):

    brew_times = {
        "Espresso":   25,
        "Latte":      30,
        "Cappuccino": 35,
        "Americano":  20,
        "Flat White": 30,
    }

    brew_time = brew_times[coffee_type]

    print(f"\n  Brewing your {coffee_type}... ", end="", flush=True)
    time.sleep(brew_time / 10)

    print(f"Ready!")
    print(f"  Beans : {beans}")
    print(f"  Milk  : {milk}")
    print(f"  Brew  : {brew_time}s")


coffee_types = ["Espresso", "Latte", "Cappuccino", "Americano", "Flat White"]

bean_types = ["Arabica", "Robusta", "Liberica", "House Blend"]

milk_types = ["Whole Milk", "Oat Milk", "Almond Milk", "Soy Milk", "No Milk"]


while True:

    print("\n☕ WELCOME TO THE COFFEE MACHINE\n")

    coffee = ask_choice("Select your coffee type:", coffee_types)

    beans = ask_choice("\nSelect your coffee beans:", bean_types)

    milk = ask_choice("\nSelect your milk type:", milk_types)

    make_coffee(coffee, beans, milk)

    print("\n")
    another = input("Order another coffee? (y/n): ").strip().lower()

    if another != "y":
        print("\nThanks for visiting! Goodbye. ☕\n")
        break
