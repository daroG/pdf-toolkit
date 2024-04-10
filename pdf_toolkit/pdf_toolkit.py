from pathlib import Path
from typing import TYPE_CHECKING, Any

from pypdf import PageObject, PdfFileReader


if TYPE_CHECKING:
    from .commands import PdfCommand


class FileSource:
    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

class PdfSource:
    def __init__(self, path: str | Path, commands: list['PdfCommand']) -> None:
        self.file_source = FileSource(path)
        self.commands = commands
        self._read_pdf_file = None
        self._result_pages: list[PageObject] = []

    @property
    def reader(self) -> PdfFileReader:
        if self._read_pdf_file is None:
            self._read_pdf_file = PdfFileReader(self.file_source)
        return self._read_pdf_file

    @property
    def last_result_pages(self) -> list[PageObject]:
        if self._result_pages == []:
            return self.reader.pages
        return self._result_pages

    @last_result_pages.setter
    def last_result_pages(self, pages: list[PageObject]) -> None:
        self._result_pages = pages


class PdfToolkit:
    def __init__(self, sources: list[PdfSource]) -> None:
        self._sources: list[PdfSource] = sources

    def execute_commands(self) -> None:
        for source in self._sources:
            for command in source.commands:
                command.execute(source)
