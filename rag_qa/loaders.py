"""Document loading: PDF (PyMuPDF), Word (python-docx) and plain text."""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Section:
    """A contiguous piece of a document with its location (page number or None)."""
    source: str
    text: str
    page: int | None = None


def _load_pdf(path: Path) -> list[Section]:
    import fitz

    with fitz.open(path) as doc:
        return [Section(path.name, page.get_text(), i + 1) for i, page in enumerate(doc)]


def _load_docx(path: Path) -> list[Section]:
    from docx import Document

    text = "\n\n".join(p.text for p in Document(path).paragraphs if p.text.strip())
    return [Section(path.name, text)]


def _load_txt(path: Path) -> list[Section]:
    return [Section(path.name, path.read_text(encoding="utf-8", errors="ignore"))]


LOADERS = {".pdf": _load_pdf, ".docx": _load_docx, ".txt": _load_txt, ".md": _load_txt}


def load_documents(folder: str | Path) -> list[Section]:
    """Load every supported file in `folder` into a flat list of Sections."""
    sections: list[Section] = []
    for path in sorted(Path(folder).iterdir()):
        loader = LOADERS.get(path.suffix.lower())
        if loader:
            sections.extend(s for s in loader(path) if s.text.strip())
    return sections
