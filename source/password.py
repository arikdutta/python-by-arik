password = ""
attempts = 0
while password != "python" and attempts < 3:
    password = input("Please enter the password: ")
    attempts = attempts + 1
if password == "python": 
    print("Access granted!")
    def verify_captcha():
        captcha = input("Please enter the captcha: ")
        if captcha == "1234":
            print("Captcha verified. Access granted!")
        else:
            print("Incorrect captcha. Access denied!")
    verify_captcha()
else:
    print("Access denied!")
    