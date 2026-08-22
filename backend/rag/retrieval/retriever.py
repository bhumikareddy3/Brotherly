from pathlib import Path

import chromadb
from chromadb.config import Settings

from rag.retrieval.embed_query import QueryEmbedder


class Retriever:

    def __init__(
        self,
        db_path=None,
        collection_name="brotherly_knowledge"
    ):

        if db_path is None:
            db_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "chroma"
            )

        self.client = chromadb.PersistentClient(
            path=str(db_path),
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        try:
            self.collection = self.client.get_collection(
                collection_name
            )

        except Exception:
            raise RuntimeError(
                f"""
Chroma collection '{collection_name}' was not found.

Make sure:

1. backend/rag/data/chroma exists
2. The collection was created by the ingestion pipeline.
"""
            )

        self.embedder = QueryEmbedder()

    def retrieve(
        self,
        query,
        top_k=5
    ):

        query_embedding = self.embedder.embed(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        retrieved_chunks = []

        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for i in range(len(ids)):

            retrieved_chunks.append({

                "chunk_id": ids[i],

                "score": round(
                    1 - distances[i],
                    4
                ),

                "text": documents[i],

                "metadata": metadatas[i]

            })

        return retrieved_chunks


if __name__ == "__main__":

    retriever = Retriever()

    question = input("Enter Question: ")

    chunks = retriever.retrieve(question)

    print("\nTop Retrieved Chunks\n")

    for chunk in chunks:

        print("=" * 70)
        print(f"ID : {chunk['chunk_id']}")
        print(f"Score : {chunk['score']}")
        print(f"Domain : {chunk['metadata']['domain']}")
        print(f"Source : {chunk['metadata']['source']}")
        print()
        print(chunk["text"][:500])
        print()