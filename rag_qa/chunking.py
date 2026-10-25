"""Split sections into overlapping, sentence-aware chunks."""
import re
from dataclasses import dataclass

from .loaders import Section


@dataclass
class Chunk:
    id: str
    text: str
    source: str
    page: int | None


def split_text(text: str, size: int = 800, overlap: int = 150) -> list[str]:
    """Greedy sentence packing up to `size` chars; the next chunk re-starts with
    roughly `overlap` chars of the previous one so context isn't cut mid-idea."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]
    chunks, current = [], []
    length = 0
    for sent in sentences:
        if current and length + len(sent) > size:
            chunks.append(" ".join(current))
            tail, tail_len = [], 0
            for s in reversed(current):
                if tail_len + len(s) > overlap:
                    break
                tail.insert(0, s)
                tail_len += len(s)
            current, length = tail, tail_len
        current.append(sent)
        length += len(sent) + 1
    if current:
        chunks.append(" ".join(current))
    return chunks


def chunk_sections(sections: list[Section], size: int = 800, overlap: int = 150) -> list[Chunk]:
    chunks = []
    for sec in sections:
        for i, piece in enumerate(split_text(sec.text, size, overlap)):
            cid = f"{sec.source}:p{sec.page or 0}:c{i}"
            chunks.append(Chunk(cid, piece, sec.source, sec.page))
    return chunks
