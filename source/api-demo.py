import requests
 
url = "https://official-joke-api.appspot.com/random_joke"
 
response = requests.get(url)
 
print(response.text)