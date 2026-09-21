from functools import lru_cache

from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def load_embedding_model():
    """
    Load the embedding model only once per process (cached).
    """
    try:
        print("Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Embedding model ready.\n")
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load embedding model: {e}")


class QueryEmbedder:

    def __init__(self):
        self.model = load_embedding_model()

    def embed(self, query):
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        return embedding.tolist()


if __name__ == "__main__":
    embedder = QueryEmbedder()
    query = input("Enter Question: ")
    vector = embedder.embed(query)
    print(f"\nEmbedding Size : {len(vector)}")
