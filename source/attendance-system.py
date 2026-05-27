"""Attendance management system with admin login and student attendance tracking."""

from getpass import getpass

USERNAME = "admin"
PASSWORD = "admin123"

attempt = 0
logged_in = False

while attempt < 3:

    username = input("Enter Username: ")
    password = getpass("Enter Password: ")

    if username == USERNAME and password == PASSWORD:
        print("Login Successful")
        logged_in = True
        break

    else:
        print("Invalid Credentials")

    attempt = attempt + 1

if not logged_in:
    print("Account Blocked")
else:
    student1 = {"id":11, "name":"Student 1","country":"Spain","age":34}
    student2 = {"id":22, "name":"Student 2","country":"France","age":28}
    student3 = {"id":33, "name":"Student 3","country":"Germany","age":42}
    student4 = {"id":24, "name":"Student 4","country":"Italy","age":36}
    student5 = {"id":25, "name":"Student 5","country":"Japan","age":29}
    students = [student1, student2, student3, student4, student5]

    total = len(students)

    present = []
    absent = []

    for student in students[:]:
        while True:
            attendance_status = input(f"Is {student['name']} from {student['country']} present? (y/n): ").strip().lower()
            if attendance_status in ("y", "n"):
                break
            print("  Invalid input! Please enter y or n only.")

        if attendance_status == "y":
            present.append(student)
            students.remove(student)
        else:
            absent.append(student)
            students.remove(student)

        print(f"  Pending  students: {', '.join(s.get('name', 'Unknown') for s in students) or 'None'}")
        print(f"  Present  students: {', '.join(s.get('name', 'Unknown') for s in present) or 'None'}")
        print(f"  Absent   students: {', '.join(s.get('name', 'Unknown') for s in absent) or 'None'}")

    print(f"Present        : {len(present)} -> {present}")
    print(f"Absent         : {len(absent)} -> {absent}")
