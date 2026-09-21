def get_recommendation(scores):

    job_score = 0
    business_score = 0
    hybrid_score = 0

    # Financial

    if scores["financial"] < 12:
        job_score += 15

    else:
        business_score += 10

    # Risk

    if scores["risk"] < 25:
        job_score += 15

    elif scores["risk"] > 40:
        business_score += 15

    else:
        hybrid_score += 10

    # Readiness

    if scores["readiness"] > 40:
        business_score += 10

    else:
        job_score += 10

    # Initiative

    if scores["initiative"] > 12:
        business_score += 10

    else:
        job_score += 5

    recommendations = {
        "Job First": job_score,
        "Business First": business_score,
        "Hybrid Later": hybrid_score
    }

    primary = max(recommendations, key=recommendations.get)

    recommendations.pop(primary)

    secondary = max(recommendations, key=recommendations.get)

    return primary, secondary