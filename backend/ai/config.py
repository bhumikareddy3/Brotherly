import os
from pathlib import Path

from dotenv import load_dotenv

# Load local .env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get_secret(key: str):
    """
    Read from environment variables (populated from .env locally,
    or from the platform's environment in production).
    """
    return os.getenv(key)


NVIDIA_API_KEY = get_secret("NVIDIA_API_KEY")
