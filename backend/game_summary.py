from matchup_features import get_matchup_features
from predict_game import predict_game
from player_predictions import predict_player_points


def get_game_summary(team1, team2, team1_players, team2_players, season="2025-26"):
    matchup = get_matchup_features(team1, team2, season)
    game_prediction = predict_game(matchup)

    team1_player_predictions = []
    for player in team1_players:
        prediction = predict_player_points(player, season)
        if prediction:
            team1_player_predictions.append(prediction)

    team2_player_predictions = []
    for player in team2_players:
        prediction = predict_player_points(player, season)
        if prediction:
            team2_player_predictions.append(prediction)

    return {
        "matchup": {
            "team1": team1,
            "team2": team2
        },
        "prediction": game_prediction,
        "players": {
            team1: team1_player_predictions,
            team2: team2_player_predictions
        }
    }