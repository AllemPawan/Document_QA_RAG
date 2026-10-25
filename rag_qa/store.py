"""Embeddings (SentenceTransformers) + persistent Chroma vector store."""
import chromadb
from sentence_transformers import SentenceTransformer

from .chunking import Chunk

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class VectorStore:
    def __init__(self, path: str = "chroma_db", collection: str = "docs"):
        self.model = SentenceTransformer(EMBED_MODEL)
        self.col = chromadb.PersistentClient(path=path).get_or_create_collection(
            collection, metadata={"hnsw:space": "cosine"}
        )

    def _embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def add(self, chunks: list[Chunk]) -> None:
        """Upsert, so re-ingesting the same files is idempotent."""
        self.col.upsert(
            ids=[c.id for c in chunks],
            documents=[c.text for c in chunks],
            embeddings=self._embed([c.text for c in chunks]),
            metadatas=[{"source": c.source, "page": c.page or 0} for c in chunks],
        )

    def search(self, query: str, k: int = 4) -> list[dict]:
        res = self.col.query(query_embeddings=self._embed([query]), n_results=k)
        return [
            {"text": t, "source": m["source"], "page": m["page"], "score": 1 - d}
            for t, m, d in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
        ]

    def count(self) -> int:
        return self.col.count()
