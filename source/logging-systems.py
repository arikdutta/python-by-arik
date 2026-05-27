from getpass import getpass
 
correct_username = "admin"
correct_password = "admin123"
 
attempt = 0
 
while attempt < 3:
 
    username = input("Enter Username: ")
    password = getpass("Enter Password: ")
 
    if username == correct_username and password == correct_password:
 
        print("Login Successful")
        break
 
    else:
        print("Invalid Credentials")
 
    attempt = attempt + 1
 
if attempt == 3:
    print("Account Blocked")