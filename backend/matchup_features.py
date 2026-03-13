from team_data import get_team_game_logs
from features_engineering import add_team_features


def get_matchup_features(team1_name, team2_name, season="2025-26"):
    team1_df = get_team_game_logs(team1_name, season)
    team2_df = get_team_game_logs(team2_name, season)

    team1_df = add_team_features(team1_df)
    team2_df = add_team_features(team2_df)

    team1_latest = team1_df.iloc[-1]
    team2_latest = team2_df.iloc[-1]

    matchup_data = {
        "team1": team1_name,
        "team2": team2_name,

        "team1_last_5_pts": team1_latest["LAST_5_PTS"],
        "team1_last_5_reb": team1_latest["LAST_5_REB"],
        "team1_last_5_ast": team1_latest["LAST_5_AST"],
        "team1_last_5_win_pct": team1_latest["LAST_5_WIN_PCT"],

        "team2_last_5_pts": team2_latest["LAST_5_PTS"],
        "team2_last_5_reb": team2_latest["LAST_5_REB"],
        "team2_last_5_ast": team2_latest["LAST_5_AST"],
        "team2_last_5_win_pct": team2_latest["LAST_5_WIN_PCT"],
    }

    return matchup_data