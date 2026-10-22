import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("bitcoin_prices.csv")

df["date"] = pd.to_datetime(df["date"])

plt.figure(figsize=(12, 5))
plt.plot(df["date"], df["price_usd"])

plt.title("Bitcoin Price Over Time")
plt.xlabel("Date")
plt.ylabel("Price (USD)")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()