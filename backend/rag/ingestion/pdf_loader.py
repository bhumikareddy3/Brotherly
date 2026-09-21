# import fitz
# from pathlib import Path


# class PDFLoader:

#     def __init__(self, knowledge_base="knowledge_base"):
#         self.knowledge_base = Path(knowledge_base)

#     def find_pdfs(self):

#         return list(
#             self.knowledge_base.rglob("*.pdf")
#         )

#     def extract_text(self, pdf_path):

#         document = fitz.open(pdf_path)

#         text = ""

#         for page in document:
#             text += page.get_text()

#         document.close()

#         return text

#     def save_markdown(self, pdf_path, text):

#         md_path = pdf_path.with_suffix(".md")

#         with open(
#             md_path,
#             "w",
#             encoding="utf-8"
#         ) as file:

#             file.write(text)

#         return md_path

#     def process(self):

#         pdf_files = self.find_pdfs()

#         if not pdf_files:

#             print("No PDF files found.")
#             return

#         print(f"\nFound {len(pdf_files)} PDF(s)\n")

#         for pdf in pdf_files:

#             print("=" * 60)
#             print(f"Processing: {pdf.name}")

#             text = self.extract_text(pdf)

#             md_file = self.save_markdown(
#                 pdf,
#                 text
#             )

#             print(f"Saved: {md_file}")

#         print("\nKnowledge extraction completed successfully.")


# if __name__ == "__main__":

#     loader = PDFLoader()

#     loader.process()

import fitz
from pathlib import Path


class PDFLoader:

    def __init__(self, knowledge_base=None):

        base_dir = Path(__file__).resolve().parent.parent

        if knowledge_base is None:
            knowledge_base = base_dir / "knowledge_base"

        self.knowledge_base = Path(knowledge_base)

    def find_pdfs(self):

        return list(
            self.knowledge_base.rglob("*.pdf")
        )

    def extract_text(self, pdf_path):

        document = fitz.open(pdf_path)

        text = ""

        for page in document:

            text += page.get_text()

        document.close()

        return text

    def save_markdown(self, pdf_path, text):

        md_path = pdf_path.with_suffix(".md")

        with open(
            md_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(text)

        return md_path

    def process(self):

        pdf_files = self.find_pdfs()

        if not pdf_files:

            print("No PDF files found.")

            return

        print(f"\nFound {len(pdf_files)} PDF(s)\n")

        for pdf in pdf_files:

            print("=" * 60)

            print(f"Processing: {pdf.name}")

            text = self.extract_text(pdf)

            md_file = self.save_markdown(
                pdf,
                text
            )

            print(f"Saved: {md_file}")

        print("\nKnowledge extraction completed successfully.")


if __name__ == "__main__":

    loader = PDFLoader()

    loader.process()