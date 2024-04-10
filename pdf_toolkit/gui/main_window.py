from logging import getLogger, INFO
import tkinter as tk
from tkinter import LEFT, RIGHT, TOP, W, ttk

from . import RecordEntryPopup, FileList


LOGGER = getLogger()
LOGGER.setLevel(INFO)

def populate_treeview(treeview: ttk.Treeview) -> None:
    treeview.insert('', 'end', text='File 1', values=('7', '1-7'))
    treeview.insert('', 'end', text='File 2', values=('20', '1-20'))
    treeview.insert('', 'end', text='File 3', values=('30', '1-30'))


class MainWindow(tk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.parent = parent
        self._init_upper_frame()
        self._init_bottom_frame()
        self.pack()

        self._add_bindings()

    def _init_upper_frame(self) -> None:
        self.upper_frame = tk.Frame(self, width=800, height=400)
        self.upper_frame.pack(side=TOP)
        self._init_left_frame(self.upper_frame)
        self._init_right_frame(self.upper_frame)


    def _init_left_frame(self, parent: tk.Widget) -> None:
        self.left_frame = tk.Frame(parent, width=100, height=400, bg='blue')

        self.add_file_button = tk.Button(self.left_frame, width=80, text='Add file')
        self.add_file_button.pack(pady=5)
        self.copy_selection_button = tk.Button(self.left_frame, width=80, text='Copy selection')
        self.copy_selection_button.pack(pady=5)
        self.left_frame.pack(side=LEFT, fill=tk.BOTH)
        self.left_frame.pack_propagate(False)

    def _init_right_frame(self, parent: tk.Widget) -> None:
        self.right_frame = tk.Frame(parent, width=700, height=400, bg='red')
        self.right_frame.pack(side=RIGHT, fill=tk.BOTH, expand=True)
        self.right_frame.pack_propagate(False)
        self._init_treeview(self.right_frame)

    def _init_bottom_frame(self) -> None:
        self.bottom_frame = tk.Frame(self, width=800, height=200, bg='yellow')
        self.bottom_frame.pack(side=TOP, fill=tk.BOTH, expand=True)
        self.bottom_frame.pack_propagate(False)

    def _init_treeview(self, parent: tk.Widget) -> None:
        self.treeview = FileList(
            parent,
            2,
            self._handle_double_click,
        )

        populate_treeview(self.treeview)

    def _add_bindings(self) -> None:
        self.add_file_button.bind('<Button-1>', self._handle_add_file)

    def _handle_add_file(self, event: tk.Event) -> None:
        self.treeview.add_file(('File name x', '4', '1-4'))

    def _handle_double_click(self, rowid: str, column: str, is_column_editable: bool) -> None:
        print(rowid, column, is_column_editable)
        if not is_column_editable:
            return

        # get column position info
        bbox_values = self.treeview.bbox(rowid, column)
        if isinstance(bbox_values, str):
            return
        x, y, _, height = bbox_values
        pady = height // 2

        # place Entry popup properly
        values = self.treeview.get_all_row_values(rowid)
        self.entryPopup = RecordEntryPopup(self.treeview, rowid, values, 2)
        self.entryPopup.place(x=x, y=y+pady, anchor=W, relwidth=1)



root = tk.Tk()
root.geometry('800x600+100+100')
app = MainWindow(root)

if __name__ == '__main__':
    app.mainloop()
