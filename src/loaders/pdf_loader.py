from pathlib import Path

import pymupdf

from src.models import Chunk


def load_pdf(path: str | Path) -> list[Chunk]:
    path = Path(path)
    chunks = []
    with pymupdf.open(path) as doc:
        for page_number, page in enumerate(doc, start=1):
            text = page.get_text().strip()
            if text:
                chunks.append(Chunk(text=text, source=path.name, location=f"стр. {page_number}"))
    return chunks
