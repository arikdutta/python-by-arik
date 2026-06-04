import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("student_course_ratings.csv")
similarity_matrix = cosine_similarity(df.values)

# Recommend courses for student 0
student_id = 0
scores = similarity_matrix[student_id]
recommended = scores.argsort()[::-1][1:6]
print("Recommended courses:", recommended)
