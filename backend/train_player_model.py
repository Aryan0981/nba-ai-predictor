import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("../data/lebron_games.csv")

df["last5_pts_avg"] = df["PTS"].rolling(5).mean()

df = df.dropna()

X = df[["last5_pts_avg"]]
y = df["PTS"]

model = RandomForestRegressor()

model.fit(X, y)

joblib.dump(model, "../models/player_points_model.pkl")

print("Model trained!")