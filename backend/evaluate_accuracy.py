import pandas as pd
from nba_api.stats.endpoints import leaguegamelog
from predict_game import predict_game


def get_league_team_logs(season="2024-25"):
    logs = leaguegamelog.LeagueGameLog(
        player_or_team_abbreviation="T",
        season=season,
        season_type_all_star="Regular Season"
    )
    return logs.get_data_frames()[0]


def add_rolling_features(df):
    df = df.copy()
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
    df = df.sort_values(["TEAM_ID", "GAME_DATE"]).reset_index(drop=True)

    df["IS_HOME"] = df["MATCHUP"].apply(lambda x: 1 if "vs." in x else 0)
    df["WIN"] = df["WL"].apply(lambda x: 1 if x == "W" else 0)

    # Rest / scheduling features
    df["REST_DAYS"] = df.groupby("TEAM_ID")["GAME_DATE"].diff().dt.days
    df["IS_BACK_TO_BACK"] = df["REST_DAYS"].apply(
        lambda x: 1 if pd.notna(x) and x <= 1 else 0
    )

    # Last 5 rolling features
    df["LAST_5_PTS"] = df.groupby("TEAM_ID")["PTS"].transform(
        lambda s: s.shift(1).rolling(5).mean()
    )
    df["LAST_5_REB"] = df.groupby("TEAM_ID")["REB"].transform(
        lambda s: s.shift(1).rolling(5).mean()
    )
    df["LAST_5_AST"] = df.groupby("TEAM_ID")["AST"].transform(
        lambda s: s.shift(1).rolling(5).mean()
    )
    df["LAST_5_TOV"] = df.groupby("TEAM_ID")["TOV"].transform(
        lambda s: s.shift(1).rolling(5).mean()
    )
    df["LAST_5_WIN_PCT"] = df.groupby("TEAM_ID")["WIN"].transform(
        lambda s: s.shift(1).rolling(5).mean()
    )

    # Last 10 rolling features
    df["LAST_10_PTS"] = df.groupby("TEAM_ID")["PTS"].transform(
        lambda s: s.shift(1).rolling(10).mean()
    )
    df["LAST_10_REB"] = df.groupby("TEAM_ID")["REB"].transform(
        lambda s: s.shift(1).rolling(10).mean()
    )
    df["LAST_10_AST"] = df.groupby("TEAM_ID")["AST"].transform(
        lambda s: s.shift(1).rolling(10).mean()
    )
    df["LAST_10_TOV"] = df.groupby("TEAM_ID")["TOV"].transform(
        lambda s: s.shift(1).rolling(10).mean()
    )
    df["LAST_10_WIN_PCT"] = df.groupby("TEAM_ID")["WIN"].transform(
        lambda s: s.shift(1).rolling(10).mean()
    )

    # Last 3 form
    df["LAST_3_WIN_PCT"] = df.groupby("TEAM_ID")["WIN"].transform(
        lambda s: s.shift(1).rolling(3).mean()
    )

    # Home / away split win rates using only prior games
    df["HOME_WIN_ONLY"] = df.apply(
        lambda row: row["WIN"] if row["IS_HOME"] == 1 else None, axis=1
    )
    df["AWAY_WIN_ONLY"] = df.apply(
        lambda row: row["WIN"] if row["IS_HOME"] == 0 else None, axis=1
    )

    df["HOME_WIN_PCT"] = df.groupby("TEAM_ID")["HOME_WIN_ONLY"].transform(
        lambda s: s.shift(1).rolling(5, min_periods=1).mean()
    )
    df["AWAY_WIN_PCT"] = df.groupby("TEAM_ID")["AWAY_WIN_ONLY"].transform(
        lambda s: s.shift(1).rolling(5, min_periods=1).mean()
    )

    df = df.drop(columns=["HOME_WIN_ONLY", "AWAY_WIN_ONLY"])

    return df


def build_matchup_rows(df):
    results = []

    for game_id, game_rows in df.groupby("GAME_ID"):
        if len(game_rows) != 2:
            continue

        home_rows = game_rows[game_rows["IS_HOME"] == 1]
        away_rows = game_rows[game_rows["IS_HOME"] == 0]

        if home_rows.empty or away_rows.empty:
            continue

        home = home_rows.iloc[0]
        away = away_rows.iloc[0]

        required_cols = [
            "LAST_5_PTS",
            "LAST_5_REB",
            "LAST_5_AST",
            "LAST_5_TOV",
            "LAST_5_WIN_PCT",
            "LAST_10_PTS",
            "LAST_10_REB",
            "LAST_10_AST",
            "LAST_10_TOV",
            "LAST_10_WIN_PCT",
            "LAST_3_WIN_PCT",
            "HOME_WIN_PCT",
            "AWAY_WIN_PCT",
            "REST_DAYS",
            "IS_BACK_TO_BACK",
        ]

        if any(pd.isna(home[col]) for col in required_cols):
            continue
        if any(pd.isna(away[col]) for col in required_cols):
            continue

        matchup_data = {
            "team1": home["TEAM_NAME"],
            "team2": away["TEAM_NAME"],

            # Team 1 raw stats
            "team1_last_5_pts": home["LAST_5_PTS"],
            "team1_last_5_reb": home["LAST_5_REB"],
            "team1_last_5_ast": home["LAST_5_AST"],
            "team1_last_5_tov": home["LAST_5_TOV"],
            "team1_last_5_win_pct": home["LAST_5_WIN_PCT"],

            "team1_last_10_pts": home["LAST_10_PTS"],
            "team1_last_10_reb": home["LAST_10_REB"],
            "team1_last_10_ast": home["LAST_10_AST"],
            "team1_last_10_tov": home["LAST_10_TOV"],
            "team1_last_10_win_pct": home["LAST_10_WIN_PCT"],

            "team1_last_3_win_pct": home["LAST_3_WIN_PCT"],
            "team1_home_win_pct": home["HOME_WIN_PCT"],
            "team1_away_win_pct": home["AWAY_WIN_PCT"],
            "team1_rest_days": home["REST_DAYS"],
            "team1_back_to_back": home["IS_BACK_TO_BACK"],

            # Team 2 raw stats
            "team2_last_5_pts": away["LAST_5_PTS"],
            "team2_last_5_reb": away["LAST_5_REB"],
            "team2_last_5_ast": away["LAST_5_AST"],
            "team2_last_5_tov": away["LAST_5_TOV"],
            "team2_last_5_win_pct": away["LAST_5_WIN_PCT"],

            "team2_last_10_pts": away["LAST_10_PTS"],
            "team2_last_10_reb": away["LAST_10_REB"],
            "team2_last_10_ast": away["LAST_10_AST"],
            "team2_last_10_tov": away["LAST_10_TOV"],
            "team2_last_10_win_pct": away["LAST_10_WIN_PCT"],

            "team2_last_3_win_pct": away["LAST_3_WIN_PCT"],
            "team2_home_win_pct": away["HOME_WIN_PCT"],
            "team2_away_win_pct": away["AWAY_WIN_PCT"],
            "team2_rest_days": away["REST_DAYS"],
            "team2_back_to_back": away["IS_BACK_TO_BACK"],

            # Difference features
            "diff_last_5_pts": home["LAST_5_PTS"] - away["LAST_5_PTS"],
            "diff_last_5_reb": home["LAST_5_REB"] - away["LAST_5_REB"],
            "diff_last_5_ast": home["LAST_5_AST"] - away["LAST_5_AST"],
            "diff_last_5_tov": home["LAST_5_TOV"] - away["LAST_5_TOV"],
            "diff_last_5_win_pct": home["LAST_5_WIN_PCT"] - away["LAST_5_WIN_PCT"],

            "diff_last_10_pts": home["LAST_10_PTS"] - away["LAST_10_PTS"],
            "diff_last_10_reb": home["LAST_10_REB"] - away["LAST_10_REB"],
            "diff_last_10_ast": home["LAST_10_AST"] - away["LAST_10_AST"],
            "diff_last_10_tov": home["LAST_10_TOV"] - away["LAST_10_TOV"],
            "diff_last_10_win_pct": home["LAST_10_WIN_PCT"] - away["LAST_10_WIN_PCT"],

            "diff_last_3_win_pct": home["LAST_3_WIN_PCT"] - away["LAST_3_WIN_PCT"],
            "diff_rest_days": home["REST_DAYS"] - away["REST_DAYS"],
            "diff_back_to_back": home["IS_BACK_TO_BACK"] - away["IS_BACK_TO_BACK"],

            "home_team_flag": 1,
            "diff_home_away_win_pct": home["HOME_WIN_PCT"] - away["AWAY_WIN_PCT"],
        }

        prediction = predict_game(matchup_data)
        predicted_winner = prediction["predicted_winner"]

        actual_winner = home["TEAM_NAME"] if home["WIN"] == 1 else away["TEAM_NAME"]
        is_correct = predicted_winner == actual_winner

        results.append({
            "GAME_ID": game_id,
            "GAME_DATE": home["GAME_DATE"].strftime("%Y-%m-%d"),
            "HOME_TEAM": home["TEAM_NAME"],
            "AWAY_TEAM": away["TEAM_NAME"],
            "PREDICTED_WINNER": predicted_winner,
            "ACTUAL_WINNER": actual_winner,
            "CORRECT": is_correct
        })

    return pd.DataFrame(results)


def evaluate_model(season="2024-25"):
    raw_df = get_league_team_logs(season)
    featured_df = add_rolling_features(raw_df)
    results_df = build_matchup_rows(featured_df)

    if results_df.empty:
        print("No evaluation results were generated.")
        return

    total_games = len(results_df)
    correct_predictions = results_df["CORRECT"].sum()
    accuracy = (correct_predictions / total_games) * 100

    print(f"Season evaluated: {season}")
    print(f"Games tested: {total_games}")
    print(f"Correct predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.2f}%")

    print("\nSample results:")
    print(results_df.head(10))

    results_df.to_csv(f"accuracy_results_{season}.csv", index=False)
    print(f"\nSaved results to accuracy_results_{season}.csv")


if __name__ == "__main__":
    evaluate_model("2024-25")