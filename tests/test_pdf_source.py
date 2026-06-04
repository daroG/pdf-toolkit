from collections.abc import Callable
from pathlib import Path

from pdf_toolkit.commands import PdfCutCommand
from pdf_toolkit.pdf_source import PdfSource


def test_last_result_pages_defaults_to_all_reader_pages(make_pdf: Callable[..., Path]):
    source = PdfSource(make_pdf(3))
    assert len(source.last_result_pages) == 3


def test_cut_selecting_no_pages_yields_empty_result(make_pdf: Callable[..., Path]):
    # Page expression '99' matches nothing in a 3-page document. The result must
    # be empty, not silently fall back to the entire document.
    source = PdfSource(make_pdf(3))
    PdfCutCommand('99').execute(source)
    assert source.last_result_pages == []


def test_cut_selecting_some_pages_keeps_only_those(make_pdf: Callable[..., Path]):
    source = PdfSource(make_pdf(5))
    PdfCutCommand('1,3').execute(source)
    assert len(source.last_result_pages) == 2
