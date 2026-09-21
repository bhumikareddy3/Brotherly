import time

from openai import OpenAI

from ai.config import NVIDIA_API_KEY
from database.db import get_recent_chats

from rag.retrieval.context_builder import ContextBuilder
from rag.prompts.prompt_builder import PromptBuilder


_client = None


def get_client():
    """Lazily create the OpenAI client so the API can boot (and serve
    non-mentor endpoints) even before an NVIDIA_API_KEY is configured."""
    global _client
    if _client is None:
        _client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=NVIDIA_API_KEY or "missing-key",
        )
    return _client


class BrotherlyMentor:

    def __init__(self):
        print("Initializing Brotherly Mentor...")

        try:
            from rag.retrieval.retriever import Retriever
            self.retriever = Retriever()
        except Exception as e:
            print(f"Retriever unavailable: {e}")
            self.retriever = None

        self.context_builder = ContextBuilder()
        self.prompt_builder = PromptBuilder()

        print("Brotherly Mentor Ready.\n")

    def _build_memory(self, limit=2):
        recent_chats = get_recent_chats(limit)

        if not recent_chats:
            return ""

        memory = ""
        for user_msg, ai_msg in recent_chats:
            memory += f"User: {user_msg[:200]}\nBrotherly: {ai_msg[:400]}\n\n"

        return memory

    def get_response(self, user_message, assessment_context=None):
        if assessment_context is None:
            assessment_context = {}

        try:
            print("=" * 80)
            print("NEW QUESTION")
            print(user_message)
            print("=" * 80)

            # --------------------------------------------------
            # Retrieval
            # --------------------------------------------------
            knowledge_context = ""

            if self.retriever is not None:
                start = time.time()
                retrieved_chunks = self.retriever.retrieve(query=user_message, top_k=5)
                print(f"Retriever Time : {time.time()-start:.2f} sec")

                if len(retrieved_chunks) > 0 and retrieved_chunks[0]["score"] < 0.20:
                    print("Low similarity detected. Skipping Knowledge Base.\n")
                else:
                    start = time.time()
                    knowledge_context = self.context_builder.build(retrieved_chunks)
                    print(f"Context Builder : {time.time()-start:.2f} sec")
            else:
                print("Retriever unavailable. Using LLM only.")

            print(f"Knowledge Context Size : {len(knowledge_context)}")

            # --------------------------------------------------
            # Conversation Memory
            # --------------------------------------------------
            conversation_memory = self._build_memory()

            # --------------------------------------------------
            # Prompt Builder
            # --------------------------------------------------
            start = time.time()
            messages = self.prompt_builder.build(
                question=user_message,
                knowledge_context=knowledge_context,
                assessment_context=assessment_context,
                conversation_memory=conversation_memory
            )
            print(f"Prompt Builder : {time.time()-start:.2f} sec")

            total_chars = sum(len(message["content"]) for message in messages)
            print(f"Prompt Size : {total_chars} characters")

            # --------------------------------------------------
            # LLM
            # --------------------------------------------------
            start = time.time()
            response = get_client().chat.completions.create(
                model="deepseek-ai/deepseek-v4-flash",
                messages=messages,
                temperature=0.3,
                top_p=1,
                max_tokens=1000,
                stream=False
            )
            print(f"LLM Time : {time.time()-start:.2f} sec")
            print("=" * 80)
            print("REQUEST COMPLETED")
            print("=" * 80)

            message = response.choices[0].message

            if message.content:
                return message.content

            return "Brotherly couldn't generate a complete response."

        except Exception as e:
            error = str(e)
            print(error)

            if "ResourceExhausted" in error or "503" in error:
                return (
                    "Brotherly is currently receiving a high volume of requests. "
                    "Please wait a few minutes and try again."
                )

            if "401" in error:
                return (
                    "Brotherly couldn't authenticate with the AI service. "
                    "Please verify the NVIDIA API key."
                )

            if "429" in error:
                return "Too many requests were sent to the AI service. Please try again shortly."

            return "Brotherly is temporarily unavailable. Please try again later."


# --------------------------------------------------
# Process-level singleton (replaces st.cache_resource)
# --------------------------------------------------
_mentor_instance = None


def get_mentor():
    global _mentor_instance
    if _mentor_instance is None:
        _mentor_instance = BrotherlyMentor()
    return _mentor_instance


def get_mentor_response(user_message, assessment_context=None):
    mentor = get_mentor()
    return mentor.get_response(user_message, assessment_context)
