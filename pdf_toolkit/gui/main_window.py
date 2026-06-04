import tkinter as tk
from tkinter import filedialog as fd, LEFT, messagebox as mb, RIGHT, TOP

from pdf_toolkit.commands import PdfCutCommand
from pdf_toolkit.exceptions import PdfToolkitError
from pdf_toolkit.pdf_source import PdfSource
from pdf_toolkit.pdf_toolkit import PdfToolkit

from .file_list import FileList


class MainWindow(tk.Frame):
    """
    Main window widget.
    """

    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.parent = parent
        self._init_upper_frame()
        self._init_bottom_frame()
        self.pack()

        parent.title('PDF merging toolkit')
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
        self.delete_selection_button = tk.Button(self.left_frame, width=80, text='Delete selection')
        self.delete_selection_button.pack(pady=5)
        self.save_button = tk.Button(self.left_frame, width=80, text='Save')
        self.save_button.pack(pady=5)
        self.left_frame.pack(side=LEFT, fill=tk.BOTH)
        self.left_frame.pack_propagate(flag=False)

    def _init_right_frame(self, parent: tk.Widget) -> None:
        self.right_frame = tk.Frame(parent, width=700, height=400, bg='red')
        self.right_frame.pack(side=RIGHT, fill=tk.BOTH, expand=True)
        self.right_frame.pack_propagate(flag=False)
        self._init_treeview(self.right_frame)

    def _init_bottom_frame(self) -> None:
        self.bottom_frame = tk.Frame(self, width=800, height=200, bg='yellow')
        self.bottom_frame.pack(side=TOP, fill=tk.BOTH, expand=True)
        self.bottom_frame.pack_propagate(flag=False)

    def _init_treeview(self, parent: tk.Widget) -> None:
        self.treeview = FileList(parent)

    def _add_bindings(self) -> None:
        self.add_file_button.bind('<Button-1>', self._handle_add_file)
        self.copy_selection_button.bind('<Button-1>', self._handle_copy_file)
        self.delete_selection_button.bind('<Button-1>', self._handle_delete_file)
        self.parent.bind('<O>', self._handle_add_file)
        self.parent.bind('<o>', self._handle_add_file)
        self.treeview.bind('<Delete>', self._handle_delete_file)
        self.save_button.bind('<Button-1>', self._handle_save)

    def _handle_add_file(self, _: tk.Event) -> None:
        filenames = fd.askopenfilenames(title='Add another pdf')
        if filenames == '':
            return
        for filename in filenames:
            source = PdfSource(filename)
            self.treeview.add_file(source)

    def _handle_copy_file(self, _: tk.Event) -> None:
        files = self.treeview.get_selected_file_sources()
        for file in files:
            self.treeview.add_file(file)

    def _handle_delete_file(self, _: tk.Event) -> None:
        selected_rows = self.treeview.selection()
        for row_id in selected_rows:
            self.treeview.delete(row_id)

    def _handle_save(self, _: tk.Event) -> None:
        sources = self.treeview.get_ordered_files()
        save_pdf(sources)


def save_pdf(sources: list[PdfSource]) -> None:
    """
    Save result pdf.

    :param sources: list of PdfSources
    """
    if not sources:
        mb.showinfo(
            'No pdf sources',
            'There is no possibility to create empty pdf file.\nAdd new sources to merge them.',
        )
        return

    toolkit = PdfToolkit(sources)
    try:
        for source in sources:
            source.commands.append(PdfCutCommand(source.pages_expression))
        toolkit.execute_commands()
    except PdfToolkitError as error:
        mb.showerror('Invalid page selection', str(error))
        return

    save_to_path = fd.asksaveasfilename(
        defaultextension='.pdf',
        title='Save merged PDF',
        confirmoverwrite=True,
        filetypes=(('pdf file', '*.pdf'),),
    )
    if not save_to_path:
        return  # user cancelled the save dialog

    try:
        toolkit.save_results(save_to_path)
    except OSError as error:
        mb.showerror('Could not save PDF', str(error))


def build_app() -> MainWindow:
    """
    Build the main application window and its Tk root.

    :return: the constructed MainWindow
    """
    root = tk.Tk()
    root.geometry('800x600+100+100')
    return MainWindow(root)


if __name__ == '__main__':
    build_app().mainloop()
