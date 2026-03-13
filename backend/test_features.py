from team_data import get_team_game_logs
from features_engineering import add_team_features

df = get_team_game_logs("Los Angeles Lakers")
df = add_team_features(df)

print(df[[
    "GAME_DATE",
    "MATCHUP",
    "PTS",
    "LAST_5_PTS",
    "LAST_5_REB",
    "LAST_5_AST",
    "LAST_5_WIN_PCT",
    "IS_HOME"
]].head())