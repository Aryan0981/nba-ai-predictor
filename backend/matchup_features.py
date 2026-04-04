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

        # Team 1 raw stats
        "team1_last_5_pts": team1_latest["LAST_5_PTS"],
        "team1_last_5_reb": team1_latest["LAST_5_REB"],
        "team1_last_5_ast": team1_latest["LAST_5_AST"],
        "team1_last_5_tov": team1_latest["LAST_5_TOV"],
        "team1_last_5_win_pct": team1_latest["LAST_5_WIN_PCT"],

        "team1_last_10_pts": team1_latest["LAST_10_PTS"],
        "team1_last_10_reb": team1_latest["LAST_10_REB"],
        "team1_last_10_ast": team1_latest["LAST_10_AST"],
        "team1_last_10_tov": team1_latest["LAST_10_TOV"],
        "team1_last_10_win_pct": team1_latest["LAST_10_WIN_PCT"],

        "team1_last_3_win_pct": team1_latest["LAST_3_WIN_PCT"],
        "team1_home_win_pct": team1_latest["HOME_WIN_PCT"],
        "team1_away_win_pct": team1_latest["AWAY_WIN_PCT"],
        "team1_rest_days": team1_latest["REST_DAYS"],
        "team1_back_to_back": team1_latest["IS_BACK_TO_BACK"],

        # Team 2 raw stats
        "team2_last_5_pts": team2_latest["LAST_5_PTS"],
        "team2_last_5_reb": team2_latest["LAST_5_REB"],
        "team2_last_5_ast": team2_latest["LAST_5_AST"],
        "team2_last_5_tov": team2_latest["LAST_5_TOV"],
        "team2_last_5_win_pct": team2_latest["LAST_5_WIN_PCT"],

        "team2_last_10_pts": team2_latest["LAST_10_PTS"],
        "team2_last_10_reb": team2_latest["LAST_10_REB"],
        "team2_last_10_ast": team2_latest["LAST_10_AST"],
        "team2_last_10_tov": team2_latest["LAST_10_TOV"],
        "team2_last_10_win_pct": team2_latest["LAST_10_WIN_PCT"],

        "team2_last_3_win_pct": team2_latest["LAST_3_WIN_PCT"],
        "team2_home_win_pct": team2_latest["HOME_WIN_PCT"],
        "team2_away_win_pct": team2_latest["AWAY_WIN_PCT"],
        "team2_rest_days": team2_latest["REST_DAYS"],
        "team2_back_to_back": team2_latest["IS_BACK_TO_BACK"],

        # Difference features
        "diff_last_5_pts": team1_latest["LAST_5_PTS"] - team2_latest["LAST_5_PTS"],
        "diff_last_5_reb": team1_latest["LAST_5_REB"] - team2_latest["LAST_5_REB"],
        "diff_last_5_ast": team1_latest["LAST_5_AST"] - team2_latest["LAST_5_AST"],
        "diff_last_5_tov": team1_latest["LAST_5_TOV"] - team2_latest["LAST_5_TOV"],
        "diff_last_5_win_pct": team1_latest["LAST_5_WIN_PCT"] - team2_latest["LAST_5_WIN_PCT"],

        "diff_last_10_pts": team1_latest["LAST_10_PTS"] - team2_latest["LAST_10_PTS"],
        "diff_last_10_reb": team1_latest["LAST_10_REB"] - team2_latest["LAST_10_REB"],
        "diff_last_10_ast": team1_latest["LAST_10_AST"] - team2_latest["LAST_10_AST"],
        "diff_last_10_tov": team1_latest["LAST_10_TOV"] - team2_latest["LAST_10_TOV"],
        "diff_last_10_win_pct": team1_latest["LAST_10_WIN_PCT"] - team2_latest["LAST_10_WIN_PCT"],

        "diff_last_3_win_pct": team1_latest["LAST_3_WIN_PCT"] - team2_latest["LAST_3_WIN_PCT"],
        "diff_rest_days": team1_latest["REST_DAYS"] - team2_latest["REST_DAYS"],
        "diff_back_to_back": team1_latest["IS_BACK_TO_BACK"] - team2_latest["IS_BACK_TO_BACK"],

        # Team1 is treated as home team in your live route right now
        "home_team_flag": 1,
        "diff_home_away_win_pct": team1_latest["HOME_WIN_PCT"] - team2_latest["AWAY_WIN_PCT"],
    }

    return matchup_data