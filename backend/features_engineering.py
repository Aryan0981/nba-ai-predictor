import pandas as pd


def add_team_features(df):
    df = df.copy()

    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"], format="%b %d, %Y")
    df = df.sort_values("GAME_DATE")

    df["IS_HOME"] = df["MATCHUP"].apply(lambda x: 1 if "vs." in x else 0)

    df["LAST_5_PTS"] = df["PTS"].rolling(5).mean()
    df["LAST_5_REB"] = df["REB"].rolling(5).mean()
    df["LAST_5_AST"] = df["AST"].rolling(5).mean()
    df["LAST_5_TOV"] = df["TOV"].rolling(5).mean()

    df["WIN"] = df["WL"].apply(lambda x: 1 if x == "W" else 0)
    df["LAST_5_WIN_PCT"] = df["WIN"].rolling(5).mean()

    df = df.dropna()

    return df