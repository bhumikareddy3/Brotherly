# import json
# from pathlib import Path

# from langchain_text_splitters import RecursiveCharacterTextSplitter


# class Chunker:

#     def __init__(
#         self,
#         knowledge_base="knowledge_base",
#         output_folder="rag/data/chunks",
#         chunk_size=1200,
#         chunk_overlap=200
#     ):

#         self.knowledge_base = Path(knowledge_base)
#         self.output_folder = Path(output_folder)

#         self.output_folder.mkdir(
#             parents=True,
#             exist_ok=True
#         )

#         self.splitter = RecursiveCharacterTextSplitter(
#             chunk_size=chunk_size,
#             chunk_overlap=chunk_overlap,
#             separators=[
#                 "\n\n",
#                 "\n",
#                 ". ",
#                 "? ",
#                 "! ",
#                 " "
#             ]
#         )

#     def process_file(self, md_file):

#         with open(
#             md_file,
#             "r",
#             encoding="utf-8"
#         ) as file:

#             text = file.read()

#         chunks = self.splitter.split_text(text)

#         domain = md_file.parent.name

#         pdf_name = md_file.with_suffix(".pdf").name

#         output = []

#         for index, chunk in enumerate(chunks, start=1):

#             output.append({

#                 "chunk_number": index,

#                 "source": pdf_name,

#                 "file": md_file.name,

#                 "text": chunk

#             })

#         output_file = self.output_folder / f"{domain}_chunks.json"

#         with open(
#             output_file,
#             "w",
#             encoding="utf-8"
#         ) as file:

#             json.dump(
#                 output,
#                 file,
#                 indent=4,
#                 ensure_ascii=False
#             )

#         print(f"Saved {len(output)} chunks -> {output_file}")

#     def process(self):

#         md_files = list(
#             self.knowledge_base.rglob("*.md")
#         )

#         if not md_files:

#             print("No markdown files found.")
#             return

#         print(f"\nFound {len(md_files)} markdown files.\n")

#         for md_file in md_files:

#             print("=" * 60)
#             print(f"Processing: {md_file}")

#             self.process_file(md_file)

#         print("\nChunk generation completed successfully.")


# if __name__ == "__main__":

#     chunker = Chunker()

#     chunker.process()

import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


class Chunker:

    def __init__(
        self,
        knowledge_base=None,
        output_folder=None,
        chunk_size=1200,
        chunk_overlap=200
    ):

        base_dir = Path(__file__).resolve().parent.parent

        if knowledge_base is None:
            knowledge_base = base_dir / "knowledge_base"

        if output_folder is None:
            output_folder = base_dir / "data" / "chunks"

        self.knowledge_base = Path(knowledge_base)
        self.output_folder = Path(output_folder)

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                " "
            ]
        )

    def process_file(self, md_file):

        with open(
            md_file,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        chunks = self.splitter.split_text(text)

        domain = md_file.parent.name

        pdf_name = md_file.with_suffix(".pdf").name

        output = []

        for index, chunk in enumerate(chunks, start=1):

            output.append({

                "chunk_number": index,

                "source": pdf_name,

                "file": md_file.name,

                "text": chunk

            })

        output_file = self.output_folder / f"{domain}_chunks.json"

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                output,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Saved {len(output)} chunks -> {output_file}"
        )

    def process(self):

        md_files = list(
            self.knowledge_base.rglob("*.md")
        )

        if not md_files:

            print("No markdown files found.")

            return

        print(
            f"\nFound {len(md_files)} markdown files.\n"
        )

        for md_file in md_files:

            print("=" * 60)

            print(f"Processing: {md_file}")

            self.process_file(md_file)

        print(
            "\nChunk generation completed successfully."
        )


if __name__ == "__main__":

    chunker = Chunker()

    chunker.process()