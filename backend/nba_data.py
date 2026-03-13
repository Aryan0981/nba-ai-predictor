from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog


def get_player_game_logs(player_name, season="2025-26"):

    player_dict = players.find_players_by_full_name(player_name)

    if not player_dict:
        return None

    player_id = player_dict[0]["id"]

    gamelog = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season
    )

    df = gamelog.get_data_frames()[0]

    return df