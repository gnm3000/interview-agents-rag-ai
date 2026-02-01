from __future__ import annotations

from pathlib import Path
from typing import List

from pypdf import PdfReader


def extract_pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def load_pdfs(paths: List[Path]) -> List[str]:
    return [extract_pdf_text(path) for path in paths]
