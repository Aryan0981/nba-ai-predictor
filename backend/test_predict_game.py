from matchup_features import get_matchup_features
from predict_game import predict_game

matchup = get_matchup_features("Los Angeles Lakers", "Denver Nuggets")
prediction = predict_game(matchup)

print(prediction)