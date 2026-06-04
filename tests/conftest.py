import sys
from collections.abc import Callable
from pathlib import Path

import pytest
from PIL import Image
from pypdf import PdfWriter


# Make the repo-root scripts (main.py, jpgOptimizer.py) importable from tests.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def make_pdf(tmp_path: Path) -> Callable[[int], Path]:
    """Return a factory that writes a blank PDF with the requested page count."""

    def _make(pages: int, name: str = 'sample.pdf') -> Path:
        writer = PdfWriter()
        for _ in range(pages):
            writer.add_blank_page(width=72, height=72)
        path = tmp_path / name
        with path.open('wb') as handle:
            writer.write(handle)
        return path

    return _make


@pytest.fixture
def make_image(tmp_path: Path) -> Callable[..., Path]:
    """Return a factory that writes a small image file."""

    def _make(name: str = 'sample.png') -> Path:
        path = tmp_path / name
        Image.new('RGB', (10, 10), color='white').save(path)
        return path

    return _make
