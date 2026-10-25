"""End-to-end RAG: ingest -> retrieve -> generate a grounded, cited answer."""
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

from .chunking import chunk_sections
from .loaders import load_documents
from .store import VectorStore

load_dotenv()

SYSTEM_PROMPT = (
    "You answer questions using ONLY the numbered context passages provided. "
    "Cite the passages you rely on inline as [1], [2], etc. "
    "If the context does not contain the answer, say you don't know. Be concise."
)


class RAGSystem:
    def __init__(self, db_path: str = "chroma_db"):
        self.store = VectorStore(db_path)
        # OpenRouter exposes an OpenAI-compatible API.
        self.llm = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
        self.model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-haiku-5.5")

    def ingest(self, folder: str, chunk_size: int = 800, overlap: int = 150) -> int:
        chunks = chunk_sections(load_documents(folder), chunk_size, overlap)
        self.store.add(chunks)
        return len(chunks)

    def ask(self, question: str, k: int = 4) -> dict:
        hits = self.store.search(question, k)
        context = "\n\n".join(
            f"[{i}] ({h['source']}{', p.' + str(h['page']) if h['page'] else ''})\n{h['text']}"
            for i, h in enumerate(hits, 1)
        )
        resp = self.llm.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
            ],
        )
        answer = resp.choices[0].message.content
        # Report only passages the model actually cited; fall back to all retrieved ones.
        cited = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}
        used = [h for i, h in enumerate(hits, 1) if i in cited] or hits
        sources = sorted({h["source"] + (f" (p.{h['page']})" if h["page"] else "") for h in used})
        return {"question": question, "answer": answer, "sources": sources, "hits": hits}
