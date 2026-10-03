from src.models import Chunk


def _tail(text: str, overlap: int) -> str:
    """Последние ~overlap символов, но начиная с целого слова."""
    if len(text) <= overlap:
        return text
    tail = text[-overlap:]
    space = tail.find(" ")
    return tail[space + 1:] if space != -1 else tail


def _split_long(text: str, max_chars: int, overlap: int) -> list[str]:
    """Режет слишком длинный абзац, стараясь резать по концу предложения или пробелу."""
    parts = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            cut = max(text.rfind(". ", start, end), text.rfind(" ", start, end))
            if cut > start + max_chars // 2:
                end = cut + 1
        parts.append(text[start:end].strip())
        if end >= len(text):
            break
        new_start = max(end - overlap, start + 1)
        space = text.find(" ", new_start, end)
        start = space + 1 if space != -1 else new_start
    return [p for p in parts if p]


def split_text(text: str, max_chars: int = 1000, overlap: int = 150) -> list[str]:
    """Собирает строки/абзацы в фрагменты до max_chars, с перекрытием между фрагментами."""
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    result: list[str] = []
    current = ""

    for p in paragraphs:
        if len(p) > max_chars:
            if current:
                result.append(current)
                current = ""
            result.extend(_split_long(p, max_chars, overlap))
            continue
        if current and len(current) + 1 + len(p) > max_chars:
            result.append(current)
            tail = _tail(current, overlap)
            current = f"{tail}\n{p}" if len(tail) + 1 + len(p) <= max_chars else p
        else:
            current = f"{current}\n{p}" if current else p

    if current:
        result.append(current)
    return result


def chunk_documents(chunks: list[Chunk], max_chars: int = 1000, overlap: int = 150) -> list[Chunk]:
    """Принимает результат загрузчиков и режет крупные фрагменты на мелкие."""
    out: list[Chunk] = []
    for c in chunks:
        if len(c.text) <= max_chars:
            out.append(c)
            continue
        pieces = split_text(c.text, max_chars, overlap)
        for i, piece in enumerate(pieces, start=1):
            location = c.location if len(pieces) == 1 else f"{c.location}, часть {i}"
            out.append(Chunk(text=piece, source=c.source, location=location))
    return out
