# Tuple: fixed subject names (won't change)
subjects = ("Math", "English", "Science", "History", "Art")

# List: students in the class (can add/remove)
students = ["Alice", "Bob", "Charlie", "David"]

# Set: students who submitted homework (no duplicates)
submitted_homework = {"Alice", "Charlie", "Alice", "David"}  # Alice duplicate is removed

# Dictionary: each student's grades per subject
grades = {
    "Alice":   [95, 88, 76, 90, 85],
    "Bob":     [70, 65, 80, 55, 90],
    "Charlie": [88, 92, 95, 78, 60],
    "David":   [60, 70, 65, 72, 88],
}

# Dictionary: student name → ID
student_ids = {"Alice": 1, "Bob": 2, "Charlie": 3, "David": 4}

# --- FUNCTIONS ---

def average(scores):
    return sum(scores) / len(scores)

def get_grade_letter(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"


# --- MAIN PROGRAM ---

print("=" * 40)
print("     SCHOOL GRADE TRACKER")
print("=" * 40)

# Add a new student
new_student = "Eve"
students.append(new_student)
grades[new_student] = [82, 79, 88, 91, 74]
student_ids[new_student] = len(student_ids) + 1
print(f"\nNew student added: {new_student}")
print(f"Class list: {students}")

# Show who submitted homework
print(f"\nHomework submitted by: {submitted_homework}")
missing_homework = set(students) - submitted_homework
print(f"Missing homework:      {missing_homework}")

print(f"Student IDs and Names: {list(student_ids.items())}")

# Print report card for each student
print("\n--- REPORT CARDS ---")
for student in students:
    scores = grades[student]  # Get scores from dictionary using student name as key

    # Zip subjects (tuple) with scores to pair them
    subject_scores = list(zip(subjects, scores))

    avg = average(scores)
    letter = get_grade_letter(avg)
    homework_status = "Yes" if student in submitted_homework else "No"

    print(f"\n [{student_ids[student]}] {student}  |  Average: {avg:.1f}  |  Grade: {letter}  |  Homework: {homework_status}")
    for subject, score in subject_scores:
        print(f"  {subject} {score}")

