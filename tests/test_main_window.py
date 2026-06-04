from collections.abc import Callable
from pathlib import Path

import pytest
from pypdf import PdfReader

from pdf_toolkit.gui import main_window as mw
from pdf_toolkit.pdf_source import PdfSource


def test_importing_main_window_has_no_module_level_window():
    # Importing the module must not spawn a Tk window as a side effect.
    assert not hasattr(mw, 'app')
    assert not hasattr(mw, 'root')
    assert callable(mw.build_app)


def test_save_pdf_reports_invalid_page_expression(
    monkeypatch: pytest.MonkeyPatch, make_pdf: Callable[..., Path]
):
    shown = []
    monkeypatch.setattr(mw.mb, 'showerror', lambda *a, **k: shown.append(a))

    def _should_not_be_called(*_a, **_k):
        raise AssertionError('save dialog must not open when validation fails')

    monkeypatch.setattr(mw.fd, 'asksaveasfilename', _should_not_be_called)

    source = PdfSource(make_pdf(2))
    source.pages_expression = 'garbage'

    mw.save_pdf([source])  # must not raise

    assert shown, 'an error dialog should have been shown'


def test_save_pdf_writes_selected_pages(
    monkeypatch: pytest.MonkeyPatch, make_pdf: Callable[..., Path], tmp_path: Path
):
    out = tmp_path / 'merged.pdf'
    monkeypatch.setattr(mw.fd, 'asksaveasfilename', lambda *a, **k: str(out))

    source = PdfSource(make_pdf(5))
    source.pages_expression = '1-2'

    mw.save_pdf([source])

    assert out.exists()
    assert len(PdfReader(out).pages) == 2


def test_save_pdf_cancel_writes_nothing(
    monkeypatch: pytest.MonkeyPatch, make_pdf: Callable[..., Path], tmp_path: Path
):
    monkeypatch.setattr(mw.fd, 'asksaveasfilename', lambda *a, **k: '')

    source = PdfSource(make_pdf(2))
    source.pages_expression = 'all'

    mw.save_pdf([source])  # cancelled -> no error, no file

    # Only the source's own file exists; no merged output was written.
    assert {p.name for p in tmp_path.glob('*.pdf')} == {'sample.pdf'}
