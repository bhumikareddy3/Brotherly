# class ContextBuilder:

#     def build(self, retrieved_chunks):

#         context = "BROTHERLY KNOWLEDGE BASE\n\n"

#         for i, chunk in enumerate(retrieved_chunks, start=1):

#             context += f"""
# ==============================
# Knowledge {i}

# Source:
# {chunk['metadata']['source']}

# Domain:
# {chunk['metadata']['domain']}

# Content:
# {chunk['text']}

# """

#         return context

class ContextBuilder:

    def build(self, retrieved_chunks):

        context = "BROTHERLY KNOWLEDGE BASE\n\n"

        for i, chunk in enumerate(retrieved_chunks, start=1):

            context += f"""
==============================
Knowledge {i}

Source:
{chunk.get("metadata", {}).get("source", "Unknown")}

Domain:
{chunk.get("metadata", {}).get("domain", "Unknown")}

Content:
{chunk.get("text", "")[:700]}

"""

        return context


if __name__ == "__main__":

    from rag.retrieval.retriever import Retriever

    retriever = Retriever()

    results = retriever.retrieve(
        "How should I choose a career?"
    )

    builder = ContextBuilder()

    print(builder.build(results))