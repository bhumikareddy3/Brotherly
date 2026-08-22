# import subprocess
# import sys
# import time


# STEPS = [

#     ("PDF Loader", "rag/ingestion/pdf_loader.py"),

#     ("Text Cleaner", "rag/ingestion/text_cleaner.py"),

#     ("Chunk Generator", "rag/ingestion/chunker.py"),

#     ("Metadata Generator", "rag/ingestion/metadata.py"),

#     ("Embedding Generator", "rag/ingestion/embedder.py"),

#     ("Vector Store", "rag/ingestion/vector_store.py"),

# ]


# def run_step(name, script):

#     print("\n" + "=" * 70)
#     print(f"Running : {name}")
#     print("=" * 70)

#     start = time.time()

#     result = subprocess.run(
#         [sys.executable, script]
#     )

#     elapsed = time.time() - start

#     if result.returncode != 0:

#         print(f"\n{name} Failed.")
#         sys.exit(1)

#     print(f"\n{name} Completed in {elapsed:.2f} sec")


# def main():

#     print("=" * 70)
#     print("BROTHERLY KNOWLEDGE INGESTION PIPELINE")
#     print("=" * 70)

#     pipeline_start = time.time()

#     for name, script in STEPS:

#         run_step(name, script)

#     total = time.time() - pipeline_start

#     print("\n" + "=" * 70)
#     print("PIPELINE COMPLETED SUCCESSFULLY")
#     print("=" * 70)

#     print(f"\nTotal Time : {total:.2f} sec")


# if __name__ == "__main__":
#     main()

from pathlib import Path
import subprocess
import sys
import time

# backend/rag directory
BASE_DIR = Path(__file__).resolve().parent

STEPS = [

    ("PDF Loader", BASE_DIR / "pdf_loader.py"),

    ("Text Cleaner", BASE_DIR / "text_cleaner.py"),

    ("Chunk Generator", BASE_DIR / "chunker.py"),

    ("Metadata Generator", BASE_DIR / "metadata.py"),

    ("Embedding Generator", BASE_DIR / "embedder.py"),

    ("Vector Store", BASE_DIR / "vector_store.py"),

]


def run_step(name, script):

    print("\n" + "=" * 70)
    print(f"Running : {name}")
    print("=" * 70)

    start = time.time()

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=BASE_DIR
    )

    elapsed = time.time() - start

    if result.returncode != 0:

        print(f"\n{name} Failed.")
        sys.exit(1)

    print(f"\n{name} Completed in {elapsed:.2f} sec")


def main():

    print("=" * 70)
    print("BROTHERLY KNOWLEDGE INGESTION PIPELINE")
    print("=" * 70)

    pipeline_start = time.time()

    for name, script in STEPS:

        run_step(name, script)

    total = time.time() - pipeline_start

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(f"\nTotal Time : {total:.2f} sec")


if __name__ == "__main__":
    main()