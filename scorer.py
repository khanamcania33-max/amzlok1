def calculate_score(product):
    demand = product["demandScore"]
    margin = product["marginScore"]
    competition = 100 - product["competitionScore"]
    trend = product["trendScore"]

    score = (
        demand * 0.35 +
        margin * 0.25 +
        competition * 0.20 +
        trend * 0.20
    )

    return round(score, 2)
