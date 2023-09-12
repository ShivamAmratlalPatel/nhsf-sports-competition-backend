
def log_score(match_id, home_score, away_score, db):
    match = db.get(Match, match_id)
    match.home_score = home_score
    match.away_score = away_score
    db.add(match)
    db.commit()
