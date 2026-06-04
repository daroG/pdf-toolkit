import tkinter as tk
from collections.abc import Callable
from tkinter import ttk
from typing import Any

from .record_entry_popup import RecordEntryPopup


class EditableTreeview(ttk.Treeview):
    """
    Simple implementation of the editable treeview.
    """

    class ColumnSettings:
        """
        Column settings.
        """

        def __init__(self, label: str = '', *, editable: bool = False) -> None:
            self.label = label
            self.editable = editable

        def get(self, attr_name: str, default: Any = None) -> Any | None:  # noqa: ANN401
            """
            Get attribute value by name.

            :param attr_name: attribute name
            :param default: default value when attribute does not exist, defaults to None
            :return: attribute value or default
            """
            return getattr(self, attr_name, default)

    def __init__(
        self,
        parent: tk.Widget,
        columns: dict[str, str | dict[str, str] | ColumnSettings],
        update_function: Callable[[Any], Any] | None = None,
    ) -> None:
        self._parent = parent
        self._columns = columns
        self._columns_mapping = dict(enumerate(columns.keys()))
        self._update_function = update_function
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
        """
        Get integer value from TK raw id.

        :param row_id: TK raw id
        :return: integer id
        """
        return int(raw_id[1:], base=16)

    def _handle_edit_event(self, event: tk.Event) -> None:
        row_raw_id, column_raw_id = self.identify_row_and_column(event.x, event.y)
        if not self.is_column_editable(column_raw_id):
            return

        # get column position info
        bbox_values = self.bbox(row_raw_id, column_raw_id)
        if isinstance(bbox_values, str):
            return
        x, y, _, height = bbox_values
        pady = height // 2

        # place Entry popup properly
        values = self.get_all_row_values(row_raw_id)
        self.entryPopup = RecordEntryPopup(
            self,
            row_raw_id,
            values,
            self.translate_column_raw_id(column_raw_id),
        )
        self.entryPopup.place(x=x, y=y + pady, anchor=tk.W, relwidth=1)

    def identify_row_and_column(self, x: int, y: int) -> tuple[str, str]:
        """
        Identify row and column raw indexes under given widget coordinates.

        :param x: x coordinate
        :param y: y coordinate
        :return: tuple of row raw id and column raw id
        """
        row_raw_id = self.identify_row(y)
        column_raw_id = self.identify_column(x)
        return row_raw_id, column_raw_id

    def get_all_row_values(self, row_raw_id: str) -> tuple[str, ...]:
        """
        Get all row values.

        :param rowid: raw row id
        :return: all column by column values from specific row
        """
        text = self.item(row_raw_id, 'text')
        values = self.item(row_raw_id, 'value')
        return (text, *values)

    def is_column_editable(self, column_raw_id: str) -> bool:
        """
        Determine if column is editable.

        :param column_raw_id: column raw id
        :return: whether the column is editable
        """
        column_id = self.translate_column_raw_id(column_raw_id)
        column_settings = self._columns[self._columns_mapping[column_id]]
        if isinstance(column_settings, str):
            return False
        return column_settings.get('editable') is True

    def _flatten_columns(self, columns: dict[str, Any]) -> list[str]:
        return list(columns.keys())[1:]
