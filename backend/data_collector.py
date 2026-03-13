from nba_data import get_player_game_logs

df = get_player_game_logs("LeBron James")
df.to_csv("../data/lebron_games.csv", index=False)

print("Saved data to CSV")