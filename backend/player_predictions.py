from nba_data import get_player_game_logs


def predict_player_points(player_name, season="2025-26"):
    df = get_player_game_logs(player_name, season)

    if df is None or df.empty:
        return None

    last_5_avg = df["PTS"].head(5).mean()
    low = round(last_5_avg - 4)
    high = round(last_5_avg + 4)

    return {
        "player": player_name,
        "last_5_avg_points": round(last_5_avg, 1),
        "projected_points_range": [low, high]
    }