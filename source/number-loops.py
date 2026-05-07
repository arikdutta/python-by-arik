
    
    
dreamJob = "DATA SCIENTIST"
language = "Python"
codeStack = "JavaScript"
yearsOfExperience = 5
age = 34
for i in range(100):
 if i == age: + yearsOfExperience     
 print("I am", age, "years old and have", yearsOfExperience, "years of experience in", language, "and", codeStack)
 print("I will become", dreamJob, "at the age of", age + yearsOfExperience)
 break


numbers = [1, 4, 7, 8, 15, 20, 35, 45, 55]
for i in numbers:
    if i > 15:
        # break the loop
        break
    else:
        print(i)
        
        
name = "Arik Dutta"
count = 0
for char in name:
    if char != 'a' and char != 'A':
        continue
    else:
        count = count + 1

print('Total number of a is:', count)

# Reversed numbers using reversed() function
list1 = [10, 20, 30, 40]
for num in reversed(list1):
    print(num)

numbers = [1, 2, 3, 4, 5]
# iterate over each element in list num
for i in numbers:
    # ** exponent operator
    square = i ** 2
    print("Square of:", i, "is:", square)
    
num = [1, 4, 5, 3, 7, 8]
for i in num:
    # calculate multiplication in future if required
    pass


print("Reverse numbers using for loop")
num = 5
# start = 5
# stop = -1
# step = -1
for num in (range(num, -1, -1)):
    print(num)
    
    
rows = 5
# outer loop
for i in range(1, rows + 1):
    # inner loop
    for j in range(1, i + 1):
        print("*", end=" ")
    print('')
    
    
dialogue = "Remember, Red, hope is a good thing, maybe the best of things, and no good thing ever dies"
# split on whitespace
for word in dialogue.split():
    print(word)