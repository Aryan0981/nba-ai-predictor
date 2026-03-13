from nba_data import get_player_game_logs

df = get_player_game_logs("LeBron James")

print(df.head())