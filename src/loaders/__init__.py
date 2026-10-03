from pathlib import Path

from src.loaders.docx_loader import load_docx
from src.loaders.pdf_loader import load_pdf
from src.loaders.xlsx_loader import load_xlsx
from src.models import Chunk

LOADERS = {
    ".pdf": load_pdf,
    ".docx": load_docx,
    ".xlsx": load_xlsx,
}


def load_document(path: str | Path) -> list[Chunk]:
    path = Path(path)
    loader = LOADERS.get(path.suffix.lower())
    if loader is None:
        raise ValueError(f"Неподдерживаемый формат: {path.suffix}")
    return loader(path)
