import logging
import tkinter as tk
from typing import Any, ClassVar, Literal

from pdf_toolkit.pdf_source import PdfSource

from .draggable_treeview import DraggableTreeview
from .editable_treeview import EditableTreeview


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


class FileList(EditableTreeview, DraggableTreeview):
    """
    File list widget.
    """

    COLUMNS: ClassVar = {
        '#0': EditableTreeview.ColumnSettings('File name', editable=False),
        'total_pages': EditableTreeview.ColumnSettings('Total pages', editable=False),
        'pages_to_proccess': EditableTreeview.ColumnSettings('Pages to proccess', editable=True),
    }

    def __init__(self, parent: tk.Widget, *_: Any) -> None:  # noqa: ANN401
        super().__init__(parent, self.COLUMNS)
        self.pack(side='left', fill=tk.BOTH, expand=True)
        self._files: list[PdfSource] = []

    def add_file(self, file: PdfSource) -> None:
        """
        Add file to file list.

        :param file: file source
        """
        index = self._calculate_index(self.selection())
        self.insert('', index, text=file.name, values=(file.pages_count, f'1-{file.pages_count}'))
        self._files.append(file)

    def _calculate_index(self, selection: tuple[str, ...]) -> int | Literal['end']:
        if len(selection) == 0:
            return 'end'
        return self.index(self.selection()[-1]) + 1

    def get_ordered_files(self) -> list[PdfSource]:
        """
        Get ordered list of source files.

        :return: ordered list of files
        """
        files = []
        for row_id in self.get_children():
            file = self._get_file_source_by_row_id(row_id)
            file.pages_expresion = self.get_all_row_values(row_id)[2]
            files.append(file)
        return files

    def get_selected_file_sources(self) -> list[PdfSource]:
        """
        Get ordered list of currently selected source files.

        :return: ordered list of selected files
        """
        return [self._get_file_source_by_row_id(row_id) for row_id in self.selection()]

    def __row_id_to_list_index(self, row_id: str) -> int:
        LOGGER.info('Row id -> "%s"', row_id)
        return int(row_id[1:], base=16) - 1

    def _get_file_source_by_row_id(self, row_id: str) -> PdfSource:
        return self._files[self.__row_id_to_list_index(row_id)]

    def _remove_file(self, row_id: str) -> None:
        self.delete(row_id)
