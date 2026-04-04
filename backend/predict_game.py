def predict_game(matchup_data):
    team1_score = 0
    team2_score = 0
    team1_reasons = []
    team2_reasons = []

    # Last 5 win percentage
    if matchup_data["diff_last_5_win_pct"] > 0:
        team1_score += 3
        team1_reasons.append(f"{matchup_data['team1']} has the better recent 5-game win rate.")
    else:
        team2_score += 3
        team2_reasons.append(f"{matchup_data['team2']} has the better recent 5-game win rate.")

    # Last 10 win percentage
    if matchup_data["diff_last_10_win_pct"] > 0:
        team1_score += 3
        team1_reasons.append(f"{matchup_data['team1']} has been stronger over the last 10 games.")
    else:
        team2_score += 3
        team2_reasons.append(f"{matchup_data['team2']} has been stronger over the last 10 games.")

    # Last 3 win percentage
    if matchup_data["diff_last_3_win_pct"] > 0:
        team1_score += 2
        team1_reasons.append(f"{matchup_data['team1']} has the better very recent form over the last 3 games.")
    else:
        team2_score += 2
        team2_reasons.append(f"{matchup_data['team2']} has the better very recent form over the last 3 games.")

    # Recent scoring
    if matchup_data["diff_last_5_pts"] > 0:
        team1_score += 2
        team1_reasons.append(f"{matchup_data['team1']} has scored more over the last 5 games.")
    else:
        team2_score += 2
        team2_reasons.append(f"{matchup_data['team2']} has scored more over the last 5 games.")

    # Last 10 scoring
    if matchup_data["diff_last_10_pts"] > 0:
        team1_score += 2
        team1_reasons.append(f"{matchup_data['team1']} has been the better scoring team over the last 10 games.")
    else:
        team2_score += 2
        team2_reasons.append(f"{matchup_data['team2']} has been the better scoring team over the last 10 games.")

    # Rebounding
    if matchup_data["diff_last_5_reb"] > 0:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} has been stronger on the boards recently.")
    else:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} has been stronger on the boards recently.")

    if matchup_data["diff_last_10_reb"] > 0:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} has the stronger rebounding trend over the last 10 games.")
    else:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} has the stronger rebounding trend over the last 10 games.")

    # Assists
    if matchup_data["diff_last_5_ast"] > 0:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} is moving the ball better recently.")
    else:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} is moving the ball better recently.")

    if matchup_data["diff_last_10_ast"] > 0:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} has the better assist trend over the last 10 games.")
    else:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} has the better assist trend over the last 10 games.")

    # Turnovers - lower is better
    if matchup_data["diff_last_5_tov"] < 0:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} has protected the ball better recently.")
    else:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} has protected the ball better recently.")

    if matchup_data["diff_last_10_tov"] < 0:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} has the better long-term turnover trend.")
    else:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} has the better long-term turnover trend.")

    # Home vs away split strength
    if matchup_data["diff_home_away_win_pct"] > 0:
        team1_score += 2
        team1_reasons.append(f"{matchup_data['team1']} has the stronger home-vs-away win profile.")
    else:
        team2_score += 2
        team2_reasons.append(f"{matchup_data['team2']} has the stronger away-vs-home comparison profile.")

    # Rest days
    if matchup_data["diff_rest_days"] > 0:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} is coming in with more rest.")
    elif matchup_data["diff_rest_days"] < 0:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} is coming in with more rest.")

    # Back-to-back penalty
    if matchup_data["team1_back_to_back"] == 1 and matchup_data["team2_back_to_back"] == 0:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} avoids the back-to-back disadvantage.")
    elif matchup_data["team2_back_to_back"] == 1 and matchup_data["team1_back_to_back"] == 0:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} avoids the back-to-back disadvantage.")

    # Home-court advantage
    if matchup_data["home_team_flag"] == 1:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} has home-court advantage.")

    total_categories = 25
    winning_score = max(team1_score, team2_score)
    confidence = round((winning_score / total_categories) * 100, 1)

    if team1_score > team2_score:
        winner = matchup_data["team1"]
        reasons = team1_reasons
    elif team2_score > team1_score:
        winner = matchup_data["team2"]
        reasons = team2_reasons
    else:
        winner = "Too close to call"
        reasons = ["Both teams are performing very similarly in recent games."]
        confidence = 50.0

    # Projected score ranges
    team1_avg_pts = matchup_data["team1_last_5_pts"]
    team2_avg_pts = matchup_data["team2_last_5_pts"]

    if matchup_data["diff_rest_days"] > 0:
        team1_avg_pts += 1
    elif matchup_data["diff_rest_days"] < 0:
        team2_avg_pts += 1

    team1_score_range = [round(team1_avg_pts - 6), round(team1_avg_pts + 6)]
    team2_score_range = [round(team2_avg_pts - 6), round(team2_avg_pts + 6)]

    return {
        "team1": matchup_data["team1"],
        "team2": matchup_data["team2"],
        "team1_score": team1_score,
        "team2_score": team2_score,
        "predicted_winner": winner,
        "confidence": confidence,
        "projected_scores": {
            matchup_data["team1"]: team1_score_range,
            matchup_data["team2"]: team2_score_range
        },
        "reasons": reasons
    }