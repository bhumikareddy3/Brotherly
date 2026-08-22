# import json
# from pathlib import Path

# import chromadb
# from chromadb.config import Settings


# class VectorStore:

#     def __init__(
#         self,
#         chunk_folder="rag/data/chunks",
#         db_path="rag/data/chroma"
#     ):

#         self.chunk_folder = Path(chunk_folder)

#         self.client = chromadb.PersistentClient(
#             path=db_path,
#             settings=Settings(
#                 anonymized_telemetry=False
#             )
#         )

#         self.collection = self.client.get_or_create_collection(
#             name="brotherly_knowledge",
#             metadata={
#                 "description": "Brotherly RAG Knowledge Base"
#             }
#         )

#     def process_file(self, json_file):

#         print(f"\nProcessing {json_file.name}")

#         with open(
#             json_file,
#             "r",
#             encoding="utf-8"
#         ) as file:

#             chunks = json.load(file)

#         ids = []
#         documents = []
#         embeddings = []
#         metadatas = []

#         for chunk in chunks:

#             ids.append(
#                 chunk["chunk_id"]
#             )

#             documents.append(
#                 chunk["text"]
#             )

#             embeddings.append(
#                 chunk["embedding"]
#             )

#             metadatas.append({

#                 "domain": chunk["domain"],

#                 "source": chunk["source"],

#                 "file": chunk["file"],

#                 "chunk_number": chunk["chunk_number"],

#                 "word_count": chunk["word_count"],

#                 "character_count": chunk["character_count"]

#             })

#         self.collection.add(

#             ids=ids,

#             documents=documents,

#             embeddings=embeddings,

#             metadatas=metadatas

#         )

#         print(f"Inserted {len(ids)} vectors")

#     def process(self):

#         json_files = list(
#             self.chunk_folder.glob("*_chunks.json")
#         )

#         if not json_files:

#             print("No chunk files found.")
#             return

#         print(
#             f"\nFound {len(json_files)} chunk files."
#         )

#         for json_file in json_files:

#             self.process_file(json_file)

#         print("\nVector database created successfully.")

#         print(
#             f"\nTotal Documents : {self.collection.count()}"
#         )


# if __name__ == "__main__":

#     store = VectorStore()

#     store.process()


import json
from pathlib import Path

import chromadb
from chromadb.config import Settings


class VectorStore:

    def __init__(
        self,
        chunk_folder=None,
        db_path=None
    ):

        # Base directory -> backend/rag
        base_dir = Path(__file__).resolve().parent.parent

        if chunk_folder is None:
            chunk_folder = base_dir / "data" / "chunks"

        if db_path is None:
            db_path = base_dir / "data" / "chroma"

        self.chunk_folder = Path(chunk_folder)

        self.client = chromadb.PersistentClient(
            path=str(db_path),
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="brotherly_knowledge",
            metadata={
                "description": "Brotherly RAG Knowledge Base"
            }
        )

    def process_file(self, json_file):

        print(f"\nProcessing {json_file.name}")

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as file:

            chunks = json.load(file)

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:

            ids.append(
                chunk["chunk_id"]
            )

            documents.append(
                chunk["text"]
            )

            embeddings.append(
                chunk["embedding"]
            )

            metadatas.append({

                "domain": chunk["domain"],

                "source": chunk["source"],

                "file": chunk["file"],

                "chunk_number": chunk["chunk_number"],

                "word_count": chunk["word_count"],

                "character_count": chunk["character_count"]

            })

        try:

            self.collection.add(

                ids=ids,

                documents=documents,

                embeddings=embeddings,

                metadatas=metadatas

            )

            print(f"Inserted {len(ids)} vectors")

        except Exception as e:

            print(f"Skipping duplicate vectors: {e}")

    def process(self):

        json_files = list(
            self.chunk_folder.glob("*_chunks.json")
        )

        if not json_files:

            print("No chunk files found.")

            return

        print(
            f"\nFound {len(json_files)} chunk files."
        )

        for json_file in json_files:

            self.process_file(json_file)

        print("\nVector database created successfully.")

        print(
            f"\nTotal Documents : {self.collection.count()}"
        )


if __name__ == "__main__":

    store = VectorStore()

    store.process()