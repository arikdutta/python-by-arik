import numpy as np

arr = np.array([10, 20, 30, 40])
print ("Mean: ",np.mean(arr))
print ("sum: ",np.sum(arr))
print ("Max: ",np.max(arr))
print ("Min: ",np.min(arr))


arr1 = np.array([1, 2, 3])
print ("1D: ",arr1)

arr2 = np.array([[1, 2, 3], [4, 5, 6]])
print ("2D: ",arr2)

print(arr[0])
print(arr[2])

print(arr1[1:2])

arr = np.array([1, 2, 3])
 
print(arr + 10)
print(arr * 2)

arr = np.array([1,2,3,4,5,6])
 
new_arr = arr.reshape(3,2)
 
print(new_arr)

random_arr = np.random.randint(1, 200, 6)
print(random_arr)

student_mark = np.array([40, 45, 88, 78, 99])
print ("Highest: ",np.max(arr))
print ("Lowest: ",np.min(arr))
print ("Avg: ",np.sum(arr)/5)