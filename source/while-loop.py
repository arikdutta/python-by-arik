i = 1
while i <= 5:
    print(i)
    i += 1

#count = 1
#do 
#print(count)
#count += 1
#Until count > 5


x = 1
while x <= 5:
    print(x)
    x = x + 1
else:
    print("Done. while loop executed normally")

number = int(input('Enter any number between 100 and 500: '))
# number greater than 100 and less than 500
while number < 100 or number > 500:
    print('Incorrect number, Please enter correct number:')
    number = int(input('Enter a Number between 100 and 500: '))
else:
    print("Given Number is correct", number)
    
# reverse while loop
i = 10
while i >= 0:
    print(i, end=' ')
    i = i - 1
    
