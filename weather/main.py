import os
from dotenv import load_dotenv
import requests
import datetime as dt
from data import data
from twilio.rest import Client

load_dotenv()

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
phone_from = os.environ.get("PHONE_FROM")
phone_to = os.environ.get("PHONE_TO")

open_weather_api_key = os.environ.get("OPEN_WEATHER_API_KEY")

MY_COORDS = {"lat": os.environ.get("MY_LAT"), "lon": os.environ.get("MY_LON")}


def send_sms():
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=phone_to, from_=phone_from, body="It will rain in the next 12 hours."
    )

    print(message.sid)


def get_weather(lat, lon):
    open_weather_api = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "units": "metric", "cnt": 12, "appid": open_weather_api_key}
    response = requests.get(open_weather_api, params=params)
    results = response.json()

    return results


weather_data = get_weather(lat=MY_COORDS["lat"], lon=MY_COORDS["lon"])
# weather_data = data

print(weather_data)

for day in data["list"]:
    time = dt.datetime.fromtimestamp(day["dt"])
    description = day["weather"][0]["id"]
    print(f"{time} - {description}")

# Codes for next 12 hours
code_list = [day["weather"][0]["id"] for day in weather_data["list"]]
rain_codes = [code for code in code_list if code <= 500]
print(rain_codes)

if len(rain_codes) > 0:
    print("It will rain in the next 12 hours.")
    # send_sms()
