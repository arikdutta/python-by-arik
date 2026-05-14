
fruits = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
choice = input("please select a fruit: ")
for fruit in fruits:
    while fruit == choice:
        print("I want a", choice, "juice!")
        break
    