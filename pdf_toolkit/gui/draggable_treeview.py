import tkinter as tk
from tkinter import ttk
from typing import Any


class DraggableTreeview(ttk.Treeview):
    """
    Draggable Tree View widget.
    """

    def __init__(self, *args: Any, **kwarg: Any) -> None:  # noqa: ANN401
        super().__init__(*args, **kwarg)
        self.__add_bindings()

    def __add_bindings(self) -> None:
        self.bind('<ButtonPress-1>', self.__button_down, add='+')
        self.bind('<ButtonRelease-1>', self.__button_up, add='+')
        self.bind('<B1-Motion>', self.__move_selection, add='+')
        self.bind('<Shift-ButtonPress-1>', self.__expand_selection_to_element, add='+')
        self.bind('<Shift-ButtonRelease-1>', self.__button_up_shift, add='+')

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

    def __button_up_shift(self, *_: Any) -> None:  # noqa: ANN401
        pass

    def __move_selection(self, event: tk.Event) -> None:
        move_to = self.index(self.identify_row(event.y))
        for selected_item in self.selection():
            self.move(selected_item, '', move_to)
