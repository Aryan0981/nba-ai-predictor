def predict_game(matchup_data):
    team1_score = 0
    team2_score = 0
    team1_reasons = []
    team2_reasons = []

    # Recent points
    if matchup_data["team1_last_5_pts"] > matchup_data["team2_last_5_pts"]:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} has scored more over the last 5 games.")
    else:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} has scored more over the last 5 games.")

    # Recent rebounds
    if matchup_data["team1_last_5_reb"] > matchup_data["team2_last_5_reb"]:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} has been stronger on the boards recently.")
    else:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} has been stronger on the boards recently.")

    # Recent assists
    if matchup_data["team1_last_5_ast"] > matchup_data["team2_last_5_ast"]:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} is moving the ball better recently.")
    else:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} is moving the ball better recently.")

    # Recent win percentage
    if matchup_data["team1_last_5_win_pct"] > matchup_data["team2_last_5_win_pct"]:
        team1_score += 1
        team1_reasons.append(f"{matchup_data['team1']} has the better recent win rate.")
    else:
        team2_score += 1
        team2_reasons.append(f"{matchup_data['team2']} has the better recent win rate.")

    total_categories = 4
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