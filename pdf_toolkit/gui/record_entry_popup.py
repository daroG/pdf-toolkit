import tkinter as tk
from tkinter import ttk
from typing import Any


class RecordEntryPopup(tk.Entry):
    """
    Record entry popup.
    """

    def __init__(
        self,
        parent: ttk.Treeview,
        iid: str,
        values: tuple[str, str, str],
        column_edit_index: int = -1,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(parent, **kwargs)
        self.treeview = parent
        self.values = values
        self.iid = iid
        self.column_edit_index = column_edit_index

        self.insert(0, self.values[column_edit_index])
        self['exportselection'] = False

        self.focus_force()
        self.bind('<Return>', self._on_return)
        self.bind('<FocusOut>', self._on_return)
        self.bind('<Control-a>', self.select_all)
        self.bind('<Escape>', lambda *_: self.destroy())

    def _calc_all_values(self) -> int:
        return len(self.values)

    def _get_updated_values(self) -> tuple[str, ...]:
        if self.column_edit_index in [-1, self._calc_all_values() - 1]:
            return self.values[:-1] + (self.get(),)

        if self.column_edit_index == 0:
            return (self.get(),) + self.values[1:]

        return self.values[:self.column_edit_index] + (self.get(),) + self.values[self.column_edit_index + 1:]

    def _on_return(self, _: Any) -> None:  # noqa: ANN401
        updated_values = self._get_updated_values()

        self.treeview.item(
            self.iid,
            text=updated_values[0],
            values=updated_values[1:],
        )
        self.destroy()

    def select_all(self, *_: Any) -> str:  # noqa: ANN401
        """
        Set selection on the whole text.

        :return: 'break' to stop propagation
        """
        self.selection_range(0, 'end')
        return 'break'
