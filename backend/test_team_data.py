from team_data import get_team_game_logs

df = get_team_game_logs("Los Angeles Lakers")
print(df.head())