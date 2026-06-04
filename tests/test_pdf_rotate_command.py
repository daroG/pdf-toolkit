from collections.abc import Callable
from pathlib import Path

from pdf_toolkit.commands import PdfRotateCommand
from pdf_toolkit.pdf_source import PdfSource


def test_rotate_returns_none_per_command_contract(make_pdf: Callable[..., Path]):
    source = PdfSource(make_pdf(2))
    assert PdfRotateCommand('all', 90).execute(source) is None


def test_rotate_applies_angle_to_matching_pages(make_pdf: Callable[..., Path]):
    source = PdfSource(make_pdf(2))
    PdfRotateCommand('all', 90).execute(source)
    assert [page.rotation for page in source.last_result_pages] == [90, 90]


def test_rotate_only_touches_pages_in_range(make_pdf: Callable[..., Path]):
    source = PdfSource(make_pdf(3))
    # '1' selects only the first page (index 0).
    PdfRotateCommand('1', 90).execute(source)
    assert [page.rotation for page in source.last_result_pages] == [90, 0, 0]
