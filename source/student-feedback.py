import json

FEEDBACK_FILE = "student_feedback.txt"
NOTEBOOK_FILE = "feedback_notebook.txt"

students = [
    {"id": 1, "name": "Student 1"},
    {"id": 2, "name": "Student 2"},
    {"id": 3, "name": "Student 3"},
]

# --- Step 1: Take input and save to file ---
print("=== Student Feedback System ===\n")

feedbacks = []

for student in students:
    print(f"Feedback for {student['name']}:")
    subject = input("  Subject: ")
    rating = input("  Rating (1-5): ")
    comments = input("  Comments: ")

    entry = {
        "id": student["id"],
        "name": student["name"],
        "subject": subject,
        "rating": rating,
        "comments": comments,
    }
    feedbacks.append(entry)
    print()

# --- Step 2: Save feedbacks to file ---
file = open(FEEDBACK_FILE, "w")
for entry in feedbacks:
    file.write(f"ID      : {entry['id']}\n")
    file.write(f"Name    : {entry['name']}\n")
    file.write(f"Subject : {entry['subject']}\n")
    file.write(f"Rating  : {entry['rating']}/5\n")
    file.write(f"Comments: {entry['comments']}\n")
    file.write("-" * 30 + "\n")
file.close()
print(f"Feedback saved to '{FEEDBACK_FILE}'.\n")

# --- Step 3: Read back from the file ---
print("=== Reading Feedback File ===\n")
file = open(FEEDBACK_FILE, "r")
data = file.read()
print(data)
file.close()

# --- Step 4: Write summary to notebook ---
notebook = open(NOTEBOOK_FILE, "w")
notebook.write("=== Feedback Notebook ===\n\n")
notebook.write(f"Total students who gave feedback: {len(feedbacks)}\n\n")

for entry in feedbacks:
    notebook.write(f"{entry['name']} | {entry['subject']} | {entry['rating']} | {entry['comments']}\n")

notebook.close()
print(f"Notebook saved to '{NOTEBOOK_FILE}'.\n")

# --- Step 5: Open and read the notebook ---
print("=== Opening Feedback Notebook ===\n")
notebook = open(NOTEBOOK_FILE, "r")
notes = notebook.read()
print(notes)
notebook.close()
