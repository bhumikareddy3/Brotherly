# from pathlib import Path
# import json

# from sentence_transformers import SentenceTransformer


# class Embedder:

#     def __init__(
#         self,
#         chunk_folder="rag/data/chunks"
#     ):

#         self.chunk_folder = Path(chunk_folder)

#         print("Loading embedding model...")

#         self.model = SentenceTransformer(
#             "all-MiniLM-L6-v2"
#         )

#         print("Model loaded.\n")

#     def process_file(self, json_file):

#         with open(
#             json_file,
#             "r",
#             encoding="utf-8"
#         ) as file:

#             chunks = json.load(file)

#         print(f"Embedding {json_file.name}")

#         for chunk in chunks:

#             embedding = self.model.encode(
#                 chunk["text"],
#                 normalize_embeddings=True
#             )

#             chunk["embedding"] = embedding.tolist()

#         with open(
#             json_file,
#             "w",
#             encoding="utf-8"
#         ) as file:

#             json.dump(
#                 chunks,
#                 file,
#                 indent=4,
#                 ensure_ascii=False
#             )

#         print(
#             f"Finished -> {json_file.name}\n"
#         )

#     def process(self):

#         json_files = list(
#             self.chunk_folder.glob("*_chunks.json")
#         )

#         if not json_files:

#             print("No chunk files found.")
#             return

#         print(
#             f"Found {len(json_files)} chunk files.\n"
#         )

#         for json_file in json_files:

#             self.process_file(json_file)

#         print(
#             "Embedding generation completed successfully."
#         )


# if __name__ == "__main__":

#     embedder = Embedder()

#     embedder.process()

import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


class Embedder:

    def __init__(
        self,
        chunk_folder=None
    ):

        base_dir = Path(__file__).resolve().parent.parent

        if chunk_folder is None:
            chunk_folder = base_dir / "data" / "chunks"

        self.chunk_folder = Path(chunk_folder)

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Model loaded.\n")

    def process_file(self, json_file):

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as file:

            chunks = json.load(file)

        print(f"Embedding {json_file.name}")

        for chunk in chunks:

            embedding = self.model.encode(
                chunk["text"],
                normalize_embeddings=True
            )

            chunk["embedding"] = embedding.tolist()

        with open(
            json_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                chunks,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Finished -> {json_file.name}\n"
        )

    def process(self):

        json_files = list(
            self.chunk_folder.glob("*_chunks.json")
        )

        if not json_files:

            print("No chunk files found.")
            return

        print(
            f"Found {len(json_files)} chunk files.\n"
        )

        for json_file in json_files:

            self.process_file(json_file)

        print(
            "Embedding generation completed successfully."
        )


if __name__ == "__main__":

    embedder = Embedder()

    embedder.process()