import joblib, pandas as pd, datetime

df = pd.read_csv("bitcoin_prices.csv")

# one row per day — fixes the duplicate Oct 19 rows
df["day"] = df["date"].str[:10]
df = df.drop_duplicates(subset="day", keep="last").reset_index(drop=True)

df["change"] = df["price_usd"].pct_change() * 100   # recompute cleanly, ignore old column

last7 = df["change"].dropna().iloc[-7:].tolist()
print("last 7 daily changes:", [round(c, 2) for c in last7])

model = joblib.load("btc_model.joblib")
prob = model.predict_proba([last7])[0][1]

tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
print(f"tomorrow ({tomorrow}): {prob:.0%} chance of a big move (>1.5%)")

# commit the prediction to paper BEFORE we know the answer
with open("predictions.log", "a") as f:
    f.write(f"{tomorrow} predicted_storm_prob={prob:.2f} actual=\n")