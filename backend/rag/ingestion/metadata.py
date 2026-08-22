# import json
# from pathlib import Path


# class MetadataGenerator:

#     def __init__(self, chunk_folder="rag/data/chunks"):

#         self.chunk_folder = Path(chunk_folder)

#     def process_file(self, json_file):

#         with open(
#             json_file,
#             "r",
#             encoding="utf-8"
#         ) as file:

#             chunks = json.load(file)

#         domain = json_file.stem.replace("_chunks", "")

#         for chunk in chunks:

#             chunk["chunk_id"] = (
#                 f"{domain}_{chunk['chunk_number']:04d}"
#             )

#             chunk["domain"] = domain

#             chunk["word_count"] = len(
#                 chunk["text"].split()
#             )

#             chunk["character_count"] = len(
#                 chunk["text"]
#             )

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
#             f"Updated metadata -> {json_file.name}"
#         )

#     def process(self):

#         json_files = list(
#             self.chunk_folder.glob("*_chunks.json")
#         )

#         if not json_files:

#             print("No chunk files found.")
#             return

#         print(
#             f"\nFound {len(json_files)} chunk files.\n"
#         )

#         for json_file in json_files:

#             self.process_file(json_file)

#         print(
#             "\nMetadata generation completed successfully."
#         )


# if __name__ == "__main__":

#     generator = MetadataGenerator()

#     generator.process()


import json
from pathlib import Path


class MetadataGenerator:

    def __init__(self, chunk_folder=None):

        base_dir = Path(__file__).resolve().parent.parent

        if chunk_folder is None:
            chunk_folder = base_dir / "data" / "chunks"

        self.chunk_folder = Path(chunk_folder)

    def process_file(self, json_file):

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as file:

            chunks = json.load(file)

        domain = json_file.stem.replace("_chunks", "")

        for chunk in chunks:

            chunk["chunk_id"] = (
                f"{domain}_{chunk['chunk_number']:04d}"
            )

            chunk["domain"] = domain

            chunk["word_count"] = len(
                chunk["text"].split()
            )

            chunk["character_count"] = len(
                chunk["text"]
            )

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
            f"Updated metadata -> {json_file.name}"
        )

    def process(self):

        json_files = list(
            self.chunk_folder.glob("*_chunks.json")
        )

        if not json_files:

            print("No chunk files found.")

            return

        print(
            f"\nFound {len(json_files)} chunk files.\n"
        )

        for json_file in json_files:

            self.process_file(json_file)

        print(
            "\nMetadata generation completed successfully."
        )


if __name__ == "__main__":

    generator = MetadataGenerator()

    generator.process()