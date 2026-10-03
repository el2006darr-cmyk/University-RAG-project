import hashlib
from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

from src.models import Chunk

MODEL_NAME = "intfloat/multilingual-e5-base"
DB_PATH = "chroma_db"
COLLECTION = "documents"


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def get_collection(reset: bool = False):
    client = chromadb.PersistentClient(path=DB_PATH)
    if reset:
        try:
            client.delete_collection(COLLECTION)
        except Exception:
            pass
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def index_chunks(chunks: list[Chunk], collection) -> None:
    if not chunks:
        return
    texts = ["passage: " + c.text for c in chunks]
    embeddings = get_model().encode(
        texts, normalize_embeddings=True, batch_size=16, show_progress_bar=True
    ).tolist()
    ids = [
        hashlib.md5(f"{i}|{c.source}|{c.location}|{c.text}".encode()).hexdigest()
        for i, c in enumerate(chunks)
    ]
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source, "location": c.location} for c in chunks],
    )


def search(query: str, k: int = 3) -> list[dict]:
    collection = get_collection()
    embedding = get_model().encode(["query: " + query], normalize_embeddings=True).tolist()
    res = collection.query(query_embeddings=embedding, n_results=k)
    hits = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        hits.append({
            "text": doc,
            "source": meta["source"],
            "location": meta["location"],
            "score": 1 - dist,  # косинусное сходство, чем ближе к 1, тем лучше
        })
    return hits
