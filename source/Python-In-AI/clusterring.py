# from sklearn.cluster import KMeans
 
# customers = [
 
# [20,5000],
# [22,7000],
# [25,9000],
 
# [35,25000],
# [40,28000],
 
# [55,70000],
# [60,80000]
# ]
 
# model = KMeans(
#     n_clusters=3,
#     random_state=42
# )
 
# model.fit(customers)
 
# print(model.labels_)

from sklearn.model_selection import train_test_split
 
data = [1,2,3,4,5,6,7,8] 
 
train,test = train_test_split(
    data,
    test_size=0.25,
    random_state=60
)
 
print(train)
print(test)