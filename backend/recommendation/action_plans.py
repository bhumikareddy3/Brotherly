JOB_PLAN = [
    "Week 1 - Update Resume",
    "Week 2 - Improve Core Skill",
    "Week 3 - Apply To Opportunities",
    "Week 4 - Mock Interviews"
]

BUSINESS_PLAN = [
    "Week 1 - Validate Business Idea",
    "Week 2 - Speak To Potential Customers",
    "Week 3 - Build MVP",
    "Week 4 - Acquire First Customer"
]

HYBRID_PLAN = [
    "Week 1 - Maintain Income Source",
    "Week 2 - Research Opportunities",
    "Week 3 - Build Side Project",
    "Week 4 - Evaluate Progress"
]


def get_action_plan(recommendation):

    if recommendation == "Job First":
        return JOB_PLAN

    elif recommendation == "Business First":
        return BUSINESS_PLAN

    return HYBRID_PLAN