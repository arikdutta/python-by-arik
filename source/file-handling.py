file = open("demo.txt", "w")
file.write("Hello Arik")
file.close()


file = open("notes.txt", "w")
 
file.write("Python\n")
file.write("AI\n")
file.write("Machine Learning")
file.close()

file = open("notes.txt", "r")
data = file.read()
print(data)
 
file.close()

file = open("notes1.txt", "a")
 
file.write("\nDeep Learning")
 
file.close()