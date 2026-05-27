import requests
import time

# response = requests.get("https://api.github.com")
# print(response.text)
# data = response.json()
# print(data)

# url = "https://official-joke-api.appspot.com/random_joke"
 
# response1 = requests.get(url)
# headers = {"authorization":}

# data1 = response1.json()
# print("data1:", data1)
# print("Setup:", data1["setup"])
# print("Punchline:", data1["punchline"])

# API_URL = "https://newsapi.org/v2/top-headlines"
# API_KEY = "your_api_key_here"

# params = {
#     "country": "us",
#     "apiKey": API_KEY,
#     "pageSize": 1
# }

# response2 = requests.get(API_URL, params=params)

# if response2.status_code == 200:
#     print(response2.json())
# else:
#     print(f"Error: {response2.status_code}")
    
    
def get_stock_data():
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSCO.LON&outputsize=full&apikey=demo"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        last_refreshed = data["Meta Data"]["3. Last Refreshed"]
        price = data["Time Series (5min)"][last_refreshed]["1. open"]
        return price
    else:
        return None

while True: 
 price = get_stock_data()
 symbol = "IBM"
 if price is not None:
    print(f"{symbol}: {price}")
    time.sleep(5)
 else:
    print("Failed to retrieve data.")
    