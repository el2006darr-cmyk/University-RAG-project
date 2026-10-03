from pathlib import Path

import openpyxl

from src.models import Chunk


def load_xlsx(path: str | Path, rows_per_chunk: int = 10) -> list[Chunk]:
    path = Path(path)
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    chunks: list[Chunk] = []

    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            continue
        header = [
            str(h).strip() if h is not None else f"колонка {i + 1}"
            for i, h in enumerate(rows[0])
        ]
        data = rows[1:]

        for start in range(0, len(data), rows_per_chunk):
            part = data[start:start + rows_per_chunk]
            lines = []
            for row in part:
                pairs = [
                    f"{h}: {v}"
                    for h, v in zip(header, row)
                    if v is not None and str(v).strip() != ""
                ]
                if pairs:
                    lines.append("; ".join(pairs))
            if lines:
                first, last = start + 2, start + len(part) + 1  # номера строк как в Excel
                chunks.append(Chunk(
                    text="\n".join(lines),
                    source=path.name,
                    location=f"лист «{ws.title}», строки {first}-{last}",
                ))

    wb.close()
    return chunks
