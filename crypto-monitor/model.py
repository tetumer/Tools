import pandas as pd

df = pd.read_csv("bitcoin_analysis.csv")

# features: last 7 days of % changes
for i in range(1, 8):
    df[f"change_lag{i}"] = df["change"].shift(i)

# target: tomorrow's % change
df["target"] = (df["change"].shift(-1) > 0).astype(int)   # 1 = tomorrow up, 0 = down

df = df.dropna()
print(df.tail())
print("rows ready for training:", len(df))
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

features = [f"change_lag{i}" for i in range(1, 8)]   # our 7 inputs

split = int(len(df) * 0.7)          # 70% train, 30% test — in TIME order
X_train, X_test = df[features][:split], df[features][split:]
y_train, y_test = df["target"][:split], df["target"][split:]

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("model accuracy     :", round(accuracy_score(y_test, predictions), 3))
print("always-guess-baseline:", round(max(y_test.mean(), 1 - y_test.mean()), 3))