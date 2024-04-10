import logging
import tkinter as tk
from tkinter import ttk
from typing import Any, ClassVar

from . import RecordEntryPopup


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


class DraggableTreeview(ttk.Treeview):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.__add_bindings()

    def __add_bindings(self) -> None:
        self.bind("<ButtonPress-1>", self.__button_down, add='+')
        self.bind("<ButtonRelease-1>", self.__button_up, add='+')
        self.bind("<B1-Motion>", self.__move_selection, add='+')
        self.bind("<Shift-ButtonPress-1>", self.__expand_selection_to_element, add='+')
        self.bind("<Shift-ButtonRelease-1>", self.__button_up_shift, add='+')

    def __button_up(self, event: tk.Event) -> None:
        if self.identify_row(event.y) in self.selection():
            self.selection_set(self.identify_row(event.y))

    def __button_down(self, event: tk.Event) -> None:
        if self.identify_row(event.y) not in self.selection():
            self.selection_set(self.identify_row(event.y))

    def __expand_selection_to_element(self, event: tk.Event) -> None:
        selected_ids = [self.index(s) for s in self.selection()]
        selected_ids.append(self.index(self.identify_row(event.y)))
        selected_ids.sort()
        for row_id in range(selected_ids[0], selected_ids[-1] + 1):
            self.selection_add(self.get_children()[row_id])

    def __button_up_shift(self, *args) -> None:
        pass

    def __move_selection(self, event: tk.Event) -> None:
        move_to = self.index(self.identify_row(event.y))
        for s in self.selection():
            self.move(s, '', move_to)


class EditableTreeview(ttk.Treeview):
    """
    Simple implementation of the editable treeview.

    """

    class ColumnSettings:
        def __init__(self, label: str = '', editable: bool = False):
            self.label = label
            self.editable = editable

        def get(self, attr_name, default = None):
            return getattr(self, attr_name, default)

    def __init__(self, parent: tk.Widget, columns: dict[str, str | dict[str, str] | ColumnSettings]):
        self._parent = parent
        self._columns = columns
        self._columns_mapping = {
            idx: column_name
            for idx, column_name in enumerate(columns.keys())
        }
        super().__init__(parent, columns=self._flatten_columns(columns))

        self._add_column_headers()

        self._add_bindings()

    def _add_column_headers(self) -> None:
        for idx, settings in self._columns.items():
            if isinstance(settings, str):
                self.heading(idx, text=settings)
            else:
                self.heading(idx, text=settings.get('label', f'Column {idx}'))

    def _add_bindings(self) -> None:
        self.bind('<Double-Button-1>', self._handle_edit_event)

    @staticmethod
    def translate_column_raw_id(raw_id: str) -> int:
        return int(raw_id[1:])

    def _handle_edit_event(self, event: tk.Event) -> None:
        rowid, column = self.identify_row_and_column(event.x, event.y)
        if not self.is_column_editable(column):
            return

        # get column position info
        bbox_values = self.bbox(rowid, column)
        if isinstance(bbox_values, str):
            return
        x, y, _, height = bbox_values
        pady = height // 2

        # place Entry popup properly
        values = self.get_all_row_values(rowid)
        self.entryPopup = RecordEntryPopup(self, rowid, values, self.translate_column_raw_id(column))
        self.entryPopup.place(x=x, y=y+pady, anchor=tk.W, relwidth=1)

    def identify_row_and_column(self, x: int, y: int) -> tuple[str, str]:
        rowid = self.identify_row(y)
        column = self.identify_column(x)
        return rowid, column

    def get_all_row_values(self, rowid: str) -> tuple[str, ...]:
        text = self.item(rowid, 'text')
        values = self.item(rowid, 'value')
        return (text, *values)

    def is_column_editable(self, column_raw_id: str) -> bool:
        # column_raw_id is #1
        column_id = self.translate_column_raw_id(column_raw_id)
        column_settings = self._columns[self._columns_mapping[column_id]]
        if isinstance(column_settings, str):
            return False
        return column_settings.get('editable') == True

    def _flatten_columns(self, columns: dict[str, Any]) -> list[str]:
        return list(columns.keys())[1:]


class FileList(EditableTreeview, DraggableTreeview):

    COLUMNS: ClassVar = {
        '#0': EditableTreeview.ColumnSettings('File name', True),
        'total_pages': EditableTreeview.ColumnSettings('Total pages'),
        'pages_to_proccess': {
            'editable': True,
            'label': 'Pages to proccess',
        },
    }

    def __init__(self, parent: tk.Widget, *args):
        super().__init__(parent, self.COLUMNS)
        self.pack(side='left', fill=tk.BOTH, expand=True)

    def add_file(self, file: tuple[str, str, str]) -> None:
        index = 'end' if len(self.selection()) == 0 else (self.index(self.selection()[-1]) + 1)
        self.insert('', index, text=file[0], values=file[1:])
