for i in range(1, 11):
  if i % 2 == 0:
      print(i)
      
      
pets = ["cat", "dog", "budgie"]

for pet in pets:
    print(pet)
    
    
for i in range(len(pets)): # i will iterate over 0, 1 and 2
    pet = pets[i]
    print(pet)
    
    
for i in range(1, 11):
    if i % 2 == 0:
        print('Even Number:', i)
    else:
        print('Odd Number:', i)