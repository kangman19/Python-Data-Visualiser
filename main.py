import requests
from datetime import datetime, timedelta, timezone
import csv
import os
import pandas as pd

API_KEY = "fe5f5f129ab4477353b27aa8c72ba2d1"  
CITY = "Nairobi"  # Changeable to any city
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()


if data.get("main"):
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    description = data["weather"][0]["description"]

    utc_now = datetime.now(timezone.utc)
    timezone_offset = data["timezone"] 
    local_time = utc_now + timedelta(seconds=timezone_offset)
    date_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Weather in {CITY} on {date_time} {description}")
    print(f"Description: {description}")
    print(f"Temperature: {temp}°C (Feels like {feels_like}°C)")

      # Save to CSV
    file_exists = os.path.isfile("weather_data.csv")
    with open("weather_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date/Time", "City", "Description", "Temperature (°C)", "Feels Like (°C)"])
        writer.writerow([date_time, CITY, description, temp, feels_like])

else:
    print("Error fetching weather data. Check city name or API key.")

df = pd.read_csv("weather_data.csv", encoding="ISO-8859-1")
df = df.drop_duplicates()
df = df.dropna()
df.to_csv("weather_data_clean.csv", index=False)
print("Cleaned data saved to weather_data_clean.csv")
print(df.head())
