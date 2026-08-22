def generate_profile(data, scores):

    profile = []

    if scores["risk"] <= 20:
        profile.append(
            "You strongly value stability and predictable outcomes."
        )

    elif scores["risk"] <= 35:
        profile.append(
            "You balance stability with calculated risk-taking."
        )

    else:
        profile.append(
            "You are comfortable operating under uncertainty and taking calculated risks."
        )

    if scores["leadership"] >= 10:
        profile.append(
            "You demonstrate strong leadership tendencies."
        )

    if scores["initiative"] >= 10:
        profile.append(
            "You regularly take initiative and create opportunities."
        )

    if data["interest"] == "Technology":
        profile.append(
            "You have strong technical interests."
        )

    elif data["interest"] == "Business":
        profile.append(
            "You are naturally drawn toward business opportunities."
        )

    elif data["interest"] == "Sales":
        profile.append(
            "You enjoy persuasion, networking, and growth-oriented activities."
        )

    return profile