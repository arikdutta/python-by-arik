"""Find the highest, lowest, and average student marks using NumPy arrays."""
import numpy as np

student_name = np.array(["Student 1", "Student 2", "Student 3", "Student 4", "Student 5"])
student_mark = np.array([40, 45, 88, 78, 99])

highest_index = np.argmax(student_mark)
lowest_index = np.argmin(student_mark)

print ("Highest: ",student_name[highest_index])
print ("Lowest: ",student_name[lowest_index])
print ("Avg: ",np.mean(student_mark))