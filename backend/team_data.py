from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog


def get_team_game_logs(team_name, season="2025-26"):
    team_list = teams.get_teams()

    team_id = None
    for team in team_list:
        if team_name.lower() in team["full_name"].lower():
            team_id = team["id"]
            break

    if team_id is None:
        return None

    gamelog = teamgamelog.TeamGameLog(
        team_id=team_id,
        season=season
    )

    df = gamelog.get_data_frames()[0]
    return df