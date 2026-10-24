import requests
import csv
import os
from datetime import datetime, timezone
import pandas as pd

URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

PARAMS = {
    "vs_currency": "usd",
    "days": "365",
    "interval": "daily"
}

response = requests.get(URL, params=PARAMS, timeout=20)
response.raise_for_status()
data = response.json()


file_exists = os.path.exists("bitcoin_prices.csv")

with open("bitcoin_prices.csv", "a", newline="") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow(["timestamp", "date", "price_usd"])

    for timestamp, price in data["prices"]:
        date = datetime.fromtimestamp(
            timestamp / 1000,
            tz=timezone.utc
        ).isoformat()

        writer.writerow([timestamp, date, price])

# Clean the dataset after collecting new data
df = pd.read_csv("bitcoin_prices.csv")

df = df.drop_duplicates(
    subset=["timestamp"],
    keep="last"
)

df = df.sort_values("timestamp")

df.to_csv("bitcoin_prices.csv", index=False)

print("Total unique records:", len(df))