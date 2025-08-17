import requests
from datetime import datetime, timedelta, timezone
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

API_KEY = "fe5f5f129ab4477353b27aa8c72ba2d1"  
CITY = "Madrid"  # Changeable to any city
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

# Load + clean
df = pd.read_csv("weather_data.csv", encoding="utf-8")
df = df.drop_duplicates().dropna()
df.to_csv("weather_data.csv", index=False, encoding="utf-8")

print(df.columns.tolist())

#temperature over date/time plot
plt.figure(figsize=(10,5))
plt.plot(df["Date/Time"], df["Temperature (°C)"], marker="o", label="Temperature")
plt.plot(df["Date/Time"], df["Feels Like (°C)"], marker="x", label="Feels Like")

plt.title(f"Weather Trend in {CITY}")
plt.xlabel("Date/Time")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

#Weather condition frequency bar chart
plt.figure(figsize=(10,5))
desc_counts = df["Description"].value_counts()
desc_counts.plot(kind="bar", figsize=(10,5), title="Weather Condition Frequency")
plt.ylabel("Count")
plt.show()

#Heatmap of average temperature by hour and city
sns.set_theme(style="whitegrid")
df["Date/Time"] = pd.to_datetime(df["Date/Time"], errors="coerce")
df["Hour"] = df["Date/Time"].dt.hour
pivot = df.pivot_table(index="Hour", columns="City", values="Temperature (°C)", aggfunc="mean")
plt.figure(figsize=(12,6))
sns.heatmap(pivot, cmap="coolwarm", annot=True, fmt=".1f")
plt.title("Average Temperature by Hour and City")
plt.show()
