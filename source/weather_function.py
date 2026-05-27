import requests
import time
 
 
def get_weather(city):
 
    url = f"https://wttr.in/{city}?format=j1"
 
    response = requests.get(url)
 
    data = response.json()
 
    temp = data["current_condition"][0]["temp_C"]
 
    print(f"{city}: {temp}°C")
 
 
cities = ["Pune", "Mumbai", "Bangalore", "Goa", "Delhi"]
 
 
while True:
 
    print("\n🌍 LIVE WEATHER REPORT\n")
 
    for city in cities:
 
        get_weather(city)
 
    print("\n⏳ Waiting 15 Minutes For Next Update...\n")
 
    time.sleep(10)