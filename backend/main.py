from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from matchup_features import get_matchup_features
from predict_game import predict_game
from player_predictions import predict_player_points
from game_summary import get_game_summary
from schedule_data import get_todays_games

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "NBA AI Predictor API Running"}

@app.get("/predict-game")
def predict_game_endpoint(team1: str, team2: str):
    matchup = get_matchup_features(team1, team2)
    return predict_game(matchup)

@app.get("/predict-player")
def predict_player_endpoint(player_name: str):
    return predict_player_points(player_name)

@app.get("/game-summary")
def game_summary_endpoint(
    team1: str,
    team2: str,
    team1_players: str,
    team2_players: str
):
    team1_players_list = [player.strip() for player in team1_players.split(",")]
    team2_players_list = [player.strip() for player in team2_players.split(",")]

    return get_game_summary(
        team1,
        team2,
        team1_players_list,
        team2_players_list
    )

@app.get("/games-today")
def games_today_endpoint():
    return get_todays_games()