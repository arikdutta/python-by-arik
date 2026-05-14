from getpass import getpass 

# message = "Hello, Python"
# print(message.replace("Python", "AI"))
# print(message.split(", "))

# username = input("Enter your username: ")
# if username.lower() == "admin":
#     print("Welcome, Admin!")
    
message = input("Enter sentence: ")
words = message.__len__()
print(f"Number of characters: {words}")

password = getpass("Enter password: ")
if len(password) >= 8 and password.isupper() and password.islower() and password.isdigit():
    print("Password is strong.")
else:
    print("Password is too short. Please use at least 8 characters.")

name = "Arik"

print(name[0])
print(name[1])  # Access first character
print(name[2])  # Access second character
print(name[3])  # Access third character

print(name[0:4])  # Access first two characters
print(name.upper())  # Convert to uppercase
print(name.lower())  # Convert to lowercase
    

