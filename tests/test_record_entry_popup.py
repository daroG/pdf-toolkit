import tkinter as tk
from collections.abc import Iterator
from tkinter import ttk

import pytest

from pdf_toolkit.gui.record_entry_popup import RecordEntryPopup


@pytest.fixture
def treeview() -> Iterator[ttk.Treeview]:
    root = tk.Tk()
    try:
        tv = ttk.Treeview(root, columns=('first', 'second'))
        yield tv
    finally:
        root.destroy()


def _make_popup(treeview: ttk.Treeview) -> tuple[RecordEntryPopup, str]:
    iid = treeview.insert('', 'end', text='name', values=('1', '2'))
    popup = RecordEntryPopup(treeview, iid, ('name', '1', '2'), column_edit_index=2)
    return popup, iid


def test_return_commits_edited_value(treeview: ttk.Treeview):
    popup, iid = _make_popup(treeview)
    popup.delete(0, 'end')
    popup.insert(0, 'CHANGED')

    popup._on_return(None)

    assert treeview.item(iid, 'value')[1] == 'CHANGED'


def test_focusout_after_return_is_a_safe_noop(treeview: ttk.Treeview):
    popup, iid = _make_popup(treeview)
    popup.delete(0, 'end')
    popup.insert(0, 'CHANGED')

    popup._on_return(None)  # commits and destroys the popup
    # A trailing <FocusOut> fires _on_return again on the destroyed widget.
    popup._on_return(None)  # must not raise

    assert treeview.item(iid, 'value')[1] == 'CHANGED'


def test_escape_discards_edit(treeview: ttk.Treeview):
    popup, iid = _make_popup(treeview)
    popup.delete(0, 'end')
    popup.insert(0, 'CHANGED')

    popup._on_escape(None)  # closes without committing
    popup._on_return(None)  # trailing <FocusOut> must not commit or raise

    assert treeview.item(iid, 'value')[1] == '2'
