from ai.prompts import BROTHERLY_PROMPT


class PromptBuilder:

    def build(
        self,
        question,
        knowledge_context,
        assessment_context=None,
        conversation_memory=""
    ):

        if assessment_context is None:
            assessment_context = {}

        assessment = f"""
USER ASSESSMENT

Primary Recommendation:
{assessment_context.get("primary", "Unknown")}

Secondary Recommendation:
{assessment_context.get("secondary", "Unknown")}

Career Path:
{assessment_context.get("career_path", "Unknown")}

Scores:
{assessment_context.get("scores", {})}

Profile:
{assessment_context.get("profile", [])}
"""

        user_prompt = f"""
Use the retrieved knowledge below as the PRIMARY source of truth.

Rules:

- Answer using the Brotherly Knowledge Base whenever possible.
- Do NOT invent personal details about the user.
- If the knowledge base contains the answer, prioritize it over your general knowledge.
- Use your own knowledge only to connect ideas or explain concepts that are not explicitly covered.
- If the knowledge base does not contain the answer, clearly state that and then provide general guidance.
- Give practical, actionable advice.

====================================================

Conversation Memory

{conversation_memory}

====================================================

Brotherly Knowledge Base

{knowledge_context}

====================================================

User Question

{question}
"""

        return [

            {
                "role": "system",
                "content": BROTHERLY_PROMPT
            },

            {
                "role": "system",
                "content": assessment
            },

            {
                "role": "user",
                "content": user_prompt
            }

        ]


if __name__ == "__main__":

    builder = PromptBuilder()

    messages = builder.build(

        question="How should I choose a career?",

        knowledge_context="Career knowledge...",

        assessment_context={
            "primary": "Job First"
        }

    )

    from pprint import pprint

    pprint(messages)