from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str    # имя файла
    location: str  # страница, раздел или лист
