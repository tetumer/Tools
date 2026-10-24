import pandas as pd
import joblib

df = pd.read_csv("bitcoin_analysis.csv")

# features: last 7 days of % changes
for i in range(1, 8):
    df[f"change_lag{i}"] = df["change"].shift(i)

# target: tomorrow's % change
df["target"] = (df["change"].shift(-1).abs() > 1.5).astype(int)

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
probs = model.predict_proba(X_test)[:, 1]      # predicted chance of a big move

print("model accuracy        :", round(accuracy_score(y_test, predictions), 3))
print("always-calm baseline  :", round(max(y_test.mean(), 1 - y_test.mean()), 3))
print("avg predicted chance on actual big-move days:", round(probs[y_test == 1].mean(), 3))

joblib.dump(model, "btc_model.joblib")