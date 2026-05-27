import pandas as pd

data = pd.Series([10, 20, 30, 40])

print(data)

data1 = {"name": ["Alice", "Bob", "Charlie"], "marks": [50, 60, 80]}
df = pd.DataFrame(data1)
print(df)	
print(df['name'])


df1 = pd.read_csv("C:\\Users\\dutta\\python-by-arik\\source\\data-.csv")
print(df1)

print("Average sales:")
print(df1["sales"].mean())
 
print("Top sales:")
print(df1[df1["sales"] > 200])

data2 = {
    "Name": ["Rahul", "Priya", "Aman", "Neha"],
    "Marks": [85, 90, 78, 95]
}
 
df3 = pd.DataFrame(data2)
 
print(df3)
 
print("Average Marks:")
print(df["marks"].mean())
 
print("Top Students:")
print(df3[df3["Marks"] > 80])