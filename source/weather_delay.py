import requests
import time
 
 
def get_weather(city):
 
    try:
 
        url = f"https://wttr.in/{city}?format=j1"
 
        response = requests.get(url)
 
        data = response.json()
 
        area = data["nearest_area"][0]["areaName"][0]["value"]
 
        temp = data["current_condition"][0]["temp_C"]
 
        if area.lower() != city.lower():
 
            print(f"{city}: Invalid City Name")
 
        else:
 
            print(f"{city}: {temp}°C")
 
 
    except Exception as e:
 
        print(f"Error fetching weather for {city}")
        print(e)
 
 
cities = ["Pune", "Goa", "Delhi"]

while True:
 
    for city in cities:
 
        get_weather(city)
 
    print("\nWaiting...\n")
 
    time.sleep(10)
 