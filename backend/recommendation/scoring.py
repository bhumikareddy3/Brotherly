def calculate_scores(data):

    scores = {
        "risk": 0,
        "financial": 0,
        "readiness": 0,
        "initiative": 0,
        "leadership": 0,
        "technical": 0,
        "people": 0,
        "business": 0
    }

    # Risk

    risk_questions = [
        data.get("risk_uncertainty", 0),
        data.get("risk_opportunity", 0),
        data.get("risk_failure", 0),
        data.get("risk_relocation", 0),
        data.get("risk_decision", 0)
    ]

    scores["risk"] = sum(risk_questions)

    # Financial

    if data["savings"] == "0-3 Months":
        scores["financial"] += 2

    elif data["savings"] == "3-6 Months":
        scores["financial"] += 5

    elif data["savings"] == "6-12 Months":
        scores["financial"] += 8

    else:
        scores["financial"] += 10

    if data["dependents"] == "No":
        scores["financial"] += 5

    scores["financial"] += data["income_stability"]

    # Leadership

    if data["leadership"] == "Yes":
        scores["leadership"] = 10

    elif data["leadership"] == "Sometimes":
        scores["leadership"] = 5

    # Initiative

    if data["built_project"] == "Yes":
        scores["initiative"] += 5

    if data["sold_service"] == "Yes":
        scores["initiative"] += 5

    scores["initiative"] += data["self_discipline"]

    # Career Interests

    if data["interest"] == "Technology":
        scores["technical"] += 10

    if data["interest"] == "Business":
        scores["business"] += 10

    if data["work_type"] == "People Interaction":
        scores["people"] += 10

    # Readiness

    scores["readiness"] = (
        data["experience"] * 2
        + scores["financial"]
        + scores["initiative"]
        + scores["leadership"]
    )

    return scores