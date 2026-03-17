from nba_api.stats.endpoints import scoreboardv2
from datetime import datetime


def get_todays_games():
    today = datetime.today().strftime("%m/%d/%Y")

    scoreboard = scoreboardv2.ScoreboardV2(game_date=today)
    games_df = scoreboard.get_data_frames()[0]
    line_score_df = scoreboard.get_data_frames()[1]

    games = []
    seen_game_ids = set()

    for game_id in games_df["GAME_ID"]:
        if game_id in seen_game_ids:
            continue

        game_teams = line_score_df[line_score_df["GAME_ID"] == game_id]

        if len(game_teams) >= 2:
            away_team = game_teams.iloc[0]["TEAM_NAME"]
            home_team = game_teams.iloc[1]["TEAM_NAME"]

            games.append({
                "game_id": game_id,
                "away_team": away_team,
                "home_team": home_team
            })

            seen_game_ids.add(game_id)

    return games