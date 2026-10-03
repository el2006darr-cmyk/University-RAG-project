import sys
from pathlib import Path

from src.chunking import chunk_documents
from src.loaders import LOADERS, load_document
from src.store import get_collection, index_chunks


def main(folder: str = "data/sample") -> None:
    chunks = []
    for f in sorted(Path(folder).iterdir()):
        if f.suffix.lower() not in LOADERS:
            print("пропускаю:", f.name)
            continue
        chunks.extend(load_document(f))
    chunks = chunk_documents(chunks)
    collection = get_collection(reset=True)
    index_chunks(chunks, collection)
    print(f"Проиндексировано фрагментов: {len(chunks)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
