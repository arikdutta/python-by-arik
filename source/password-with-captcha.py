import random
import sys

def verify_captcha():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    correct_answer = a + b
    try:
        user_input = int(input(f"Solve captcha to continue: {a} + {b} = "))
    except ValueError:
        print("Invalid input. Captcha must be a number. Access denied!")
        return False

    if user_input == correct_answer:
        print("Captcha verified. Access granted!")
        return True
    else:
        print("Incorrect captcha. Access denied!")
        return False

MAX_ATTEMPTS = 3
PASSWORD = "python"

for attempt in range(1, MAX_ATTEMPTS + 1):
    password = input("Please enter the password: ")
    if password == PASSWORD:
        print("Password correct. Proceeding to captcha...")
        if verify_captcha():
            # Place any post-authentication logic here
            pass
        break
    else:
        remaining = MAX_ATTEMPTS - attempt
        if remaining > 0:
            print(f"Incorrect password. You have {remaining} attempt(s) left.")
        else:
            print("Access denied! No more attempts.")
            sys.exit(1)