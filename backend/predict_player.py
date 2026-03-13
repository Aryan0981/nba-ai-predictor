import joblib
import numpy as np

model = joblib.load("../models/player_points_model.pkl")

def predict_points(last5_avg):

    prediction = model.predict([[last5_avg]])

    return prediction[0]