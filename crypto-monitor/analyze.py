
import pandas as pd
import numpy as np

df = pd.read_csv("bitcoin_prices.csv")
df["date"] = pd.to_datetime(df["date"])

df["change"] = np.nan

for i in range(1, len(df)):
    yesterday = df.iloc[i - 1]["price_usd"]
    today = df.iloc[i]["price_usd"]

    df.loc[i, "change"] = ((today - yesterday) / yesterday) * 100

df.to_csv("bitcoin_analysis.csv", index=False)

print(df.tail(10))

average = df["change"].mean()
largest_rise = df["change"].max()
largest_fall = df["change"].min()

print("Average daily change:", average, "%")
print("Largest daily rise:", largest_rise, "%")
print("Largest daily fall:", largest_fall, "%")