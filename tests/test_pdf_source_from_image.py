from collections.abc import Callable
from pathlib import Path

from pdf_toolkit.pdf_source import PdfSourceFromImage


def test_image_source_produces_single_page(make_image: Callable[..., Path]):
    source = PdfSourceFromImage(make_image())
    assert source.pages_count == 1
    assert len(source.last_result_pages) == 1


def test_image_source_exposes_file_name(make_image: Callable[..., Path]):
    source = PdfSourceFromImage(make_image('photo.png'))
    assert source.name == 'photo.png'


def test_image_source_leaves_no_temp_file_in_cwd(make_image: Callable[..., Path]):
    before = set(Path.cwd().iterdir())
    PdfSourceFromImage(make_image())
    assert set(Path.cwd().iterdir()) == before
