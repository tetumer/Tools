import pandas as pd

df = pd.read_csv("bitcoin_analysis.csv")
df["up"] = (df["change"] > 0).astype(int)   # 1 = green day, 0 = red day

for n in range(1, 11):
    # rows where the last n days were ALL green
    streak = df["up"].rolling(n).sum() == n
    next_day = df["up"].shift(-1)           # what happened the day after
    after = next_day[streak]

    print(f"{n} green days in a row -> next day was green "
          f"{after.mean():.0%} of the time  (happened {len(after)} times)")