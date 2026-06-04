import gc
import tkinter as tk
import weakref
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from pdf_toolkit.gui.file_list import FileList
from pdf_toolkit.pdf_source import PdfSource


@pytest.fixture
def file_list() -> Iterator[FileList]:
    root = tk.Tk()
    try:
        yield FileList(root)
    finally:
        root.destroy()


def _add(file_list: FileList, make_pdf: Callable[..., Path], *names: str) -> None:
    for name in names:
        file_list.add_file(PdfSource(make_pdf(1, name)))


def test_get_ordered_files_follows_visual_order(
    file_list: FileList, make_pdf: Callable[..., Path]
):
    _add(file_list, make_pdf, 'a.pdf', 'b.pdf', 'c.pdf')
    assert [s.name for s in file_list.get_ordered_files()] == ['a.pdf', 'b.pdf', 'c.pdf']


def test_delete_drops_source_from_ordered_files(
    file_list: FileList, make_pdf: Callable[..., Path]
):
    _add(file_list, make_pdf, 'a.pdf', 'b.pdf', 'c.pdf')
    middle = file_list.get_children()[1]
    file_list.delete(middle)
    assert [s.name for s in file_list.get_ordered_files()] == ['a.pdf', 'c.pdf']


def test_deleted_source_is_released(file_list: FileList, make_pdf: Callable[..., Path]):
    file_list.add_file(PdfSource(make_pdf(1, 'a.pdf')))
    doomed = PdfSource(make_pdf(1, 'b.pdf'))
    file_list.add_file(doomed)

    ref = weakref.ref(doomed)
    file_list.delete(file_list.get_children()[1])
    del doomed
    gc.collect()

    assert ref() is None
