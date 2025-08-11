import requests
from datetime import datetime

API_KEY = "fe5f5f129ab4477353b27aa8c72ba2d1"  
CITY = "Paris"  # Changeable to any city
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()

print(data)
if data.get("main"):
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    description = data["weather"][0]["description"]

    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Weather in {CITY}: {description}")
    print(f"Temperature: {temp}°C (Feels like {feels_like}°C)")
    print(f"Date and Time: {date_time}")
else:
    print("Error fetching weather data. Check city name or API key.")
