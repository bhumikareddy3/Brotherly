def get_career_path(scores, data):

    if data["interest"] == "Technology":
        return "Technical Role Path"

    elif data["interest"] == "Sales":
        return "People-Facing Role Path"

    elif data["interest"] == "Business":
        return "Service Business Path"

    elif data["work_type"] == "Business Activities":
        return "Service Business Path"

    return "General Career Path"