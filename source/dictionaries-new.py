# ["Arik","Spain",34]
student = {"name":"Arik","country":"Spain","age":34}
print(student)
print(student["name"])  
print(student["country"])
print(student["age"])
print(student.get("salary"))  # This will return None since "salary" is not a key in the dictionary

student["salary"] = 50000
print(student)
del student["age"]
print(student)

for key in student:
    print(key)

for key, value in student.items():
    print(key, ":", value)