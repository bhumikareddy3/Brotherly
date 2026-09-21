# import re
# from pathlib import Path


# class TextCleaner:

#     def __init__(self):
#         pass

#     def clean_text(self, text: str) -> str:
#         """
#         Clean extracted PDF text while preserving structure.
#         """

#         # Normalize line endings
#         text = text.replace("\r\n", "\n")
#         text = text.replace("\r", "\n")

#         # Replace tabs with spaces
#         text = text.replace("\t", " ")

#         # Remove trailing spaces
#         text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

#         # Replace multiple spaces with one
#         text = re.sub(r"[ ]{2,}", " ", text)

#         # Replace 3+ blank lines with 2
#         text = re.sub(r"\n{3,}", "\n\n", text)

#         return text.strip()

#     def clean_file(self, md_path: Path):

#         with open(md_path, "r", encoding="utf-8") as file:
#             text = file.read()

#         cleaned_text = self.clean_text(text)

#         with open(md_path, "w", encoding="utf-8") as file:
#             file.write(cleaned_text)

#         print(f"Cleaned: {md_path}")

#     def process(self, knowledge_base="knowledge_base"):

#         root = Path(knowledge_base)

#         md_files = list(root.rglob("*.md"))

#         if not md_files:
#             print("No markdown files found.")
#             return

#         print(f"\nFound {len(md_files)} markdown file(s).\n")

#         for md in md_files:
#             self.clean_file(md)

#         print("\nText cleaning completed successfully.")


# if __name__ == "__main__":

#     cleaner = TextCleaner()

#     cleaner.process()

import re
from pathlib import Path


class TextCleaner:

    def __init__(self):
        pass

    def clean_text(self, text: str) -> str:
        """
        Clean extracted PDF text while preserving structure.
        """

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Replace tabs with spaces
        text = text.replace("\t", " ")

        # Remove trailing spaces
        text = re.sub(
            r"[ \t]+$",
            "",
            text,
            flags=re.MULTILINE
        )

        # Replace multiple spaces with one
        text = re.sub(
            r"[ ]{2,}",
            " ",
            text
        )

        # Replace 3+ blank lines with 2
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        return text.strip()

    def clean_file(self, md_path: Path):

        with open(
            md_path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        cleaned_text = self.clean_text(text)

        with open(
            md_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(cleaned_text)

        print(f"Cleaned: {md_path}")

    def process(self, knowledge_base=None):

        if knowledge_base is None:

            knowledge_base = (
                Path(__file__).resolve().parent.parent
                / "knowledge_base"
            )

        root = Path(knowledge_base)

        md_files = list(
            root.rglob("*.md")
        )

        if not md_files:

            print("No markdown files found.")

            return

        print(
            f"\nFound {len(md_files)} markdown file(s).\n"
        )

        for md in md_files:

            self.clean_file(md)

        print(
            "\nText cleaning completed successfully."
        )


if __name__ == "__main__":

    cleaner = TextCleaner()

    cleaner.process()