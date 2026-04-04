import pandas as pd


def add_team_features(df):
    df = df.copy()

    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"], format="%b %d, %Y")
    df = df.sort_values("GAME_DATE").reset_index(drop=True)

    df["IS_HOME"] = df["MATCHUP"].apply(lambda x: 1 if "vs." in x else 0)
    df["WIN"] = df["WL"].apply(lambda x: 1 if x == "W" else 0)

    # Rest-related features
    df["REST_DAYS"] = df["GAME_DATE"].diff().dt.days
    df["IS_BACK_TO_BACK"] = df["REST_DAYS"].apply(
        lambda x: 1 if pd.notna(x) and x <= 1 else 0
    )

    # Last 5 rolling features
    df["LAST_5_PTS"] = df["PTS"].shift(1).rolling(5).mean()
    df["LAST_5_REB"] = df["REB"].shift(1).rolling(5).mean()
    df["LAST_5_AST"] = df["AST"].shift(1).rolling(5).mean()
    df["LAST_5_TOV"] = df["TOV"].shift(1).rolling(5).mean()
    df["LAST_5_WIN_PCT"] = df["WIN"].shift(1).rolling(5).mean()
    df["LAST_5_FG_PCT"] = df["FG_PCT"].shift(1).rolling(5).mean()
    df["LAST_5_FG3_PCT"] = df["FG3_PCT"].shift(1).rolling(5).mean()
    df["LAST_5_FT_PCT"] = df["FT_PCT"].shift(1).rolling(5).mean()
    df["LAST_5_OREB"] = df["OREB"].shift(1).rolling(5).mean()
    df["LAST_5_DREB"] = df["DREB"].shift(1).rolling(5).mean()

    # Last 10 rolling features
    df["LAST_10_PTS"] = df["PTS"].shift(1).rolling(10).mean()
    df["LAST_10_REB"] = df["REB"].shift(1).rolling(10).mean()
    df["LAST_10_AST"] = df["AST"].shift(1).rolling(10).mean()
    df["LAST_10_TOV"] = df["TOV"].shift(1).rolling(10).mean()
    df["LAST_10_WIN_PCT"] = df["WIN"].shift(1).rolling(10).mean()
    df["LAST_10_FG_PCT"] = df["FG_PCT"].shift(1).rolling(10).mean()
    df["LAST_10_FG3_PCT"] = df["FG3_PCT"].shift(1).rolling(10).mean()
    df["LAST_10_FT_PCT"] = df["FT_PCT"].shift(1).rolling(10).mean()
    df["LAST_10_OREB"] = df["OREB"].shift(1).rolling(10).mean()
    df["LAST_10_DREB"] = df["DREB"].shift(1).rolling(10).mean()

    # Very recent form
    df["LAST_3_WIN_PCT"] = df["WIN"].shift(1).rolling(3).mean()

    # Home / away split win percentages
    df["HOME_WIN_ONLY"] = df.apply(
        lambda row: row["WIN"] if row["IS_HOME"] == 1 else None, axis=1
    )
    df["AWAY_WIN_ONLY"] = df.apply(
        lambda row: row["WIN"] if row["IS_HOME"] == 0 else None, axis=1
    )

    df["HOME_WIN_PCT"] = df["HOME_WIN_ONLY"].shift(1).rolling(5, min_periods=1).mean()
    df["AWAY_WIN_PCT"] = df["AWAY_WIN_ONLY"].shift(1).rolling(5, min_periods=1).mean()

    df = df.drop(columns=["HOME_WIN_ONLY", "AWAY_WIN_ONLY"])
    df = df.dropna().reset_index(drop=True)

    return df