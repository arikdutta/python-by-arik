student_Names = ["Alice", "Bob", "Charlie", "David", "Eve", 1233]
print(student_Names)
print(student_Names [0])  # Output: Alice
print(student_Names [1])  # Output: Bob
print(student_Names [2])  # Output: Charlie
print(student_Names [3])  # Output: David   
print(student_Names [4])  # Output: Eve 
print(student_Names [5])  # Output: 1233

student_Names = ["Alice", "Bob", "Charlie", "David", "Eve", 1233]

for name in student_Names:
    print(name)
    



student_Names.append("Frank")
print(student_Names [6]) 


fruits = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
for fruit in fruits:
    if fruit == "Cherry":
        print("I want a cherry juice!")

student_Number = int(input("Enter the number of students: "))
print(student_Names [student_Number])

student_Names.append("Frank")
student_Names.insert(0, "Grace")
print("Frank added to the list.")
print(student_Names)
student_Number = int(input("Enter the number of students: "))
print(student_Names [student_Number])

student_Names.remove(1233)
print("1233 removed from the list.")
print(student_Names)

student_Names [3]   = "Bob"
student_Names [1]   = "David"
print("David changed to Bob.")
print(student_Names)