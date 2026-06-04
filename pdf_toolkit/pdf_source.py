from functools import cached_property
from pathlib import Path

from PIL import Image
from pypdf import PageObject, PdfReader

from pdf_toolkit.commands.pdf_command import PdfCommand


class FileSource:
    """
    File source.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)


class PdfSource:
    """
    Pdf source.
    """

    def __init__(self, path: str | Path, commands: list['PdfCommand'] | None = None) -> None:
        self.file_source = FileSource(path)
        self.commands = commands or []
        self.pages_expresion = 'all'
        self._read_pdf_file = None
        self._result_pages: list[PageObject] = []

    @property
    def reader(self) -> PdfReader:
        if self._read_pdf_file is None:
            self._read_pdf_file = PdfReader(self.file_source.path)
        return self._read_pdf_file

    @property
    def last_result_pages(self) -> list[PageObject]:
        if self._result_pages == []:
            return self.reader.pages
        return self._result_pages

    @last_result_pages.setter
    def last_result_pages(self, pages: list[PageObject]) -> None:
        self._result_pages = pages

    @property
    def name(self) -> str:
        return self.file_source.path.name

    @cached_property
    def pages_count(self) -> int:
        return len(self.reader.pages)

    def __repr__(self) -> str:
        return f'<PdfSource(name={self.name})>'


class PdfSourceFromImage:
    """
    Image source.
    """

    _TMP_PDF_NAME = 'tmp_pdf_image_from_pdf_pdf_toolkit.pdf'

    def __init__(self, path: str | Path, commands: list['PdfCommand'] | None = None) -> None:
        self.file_source = FileSource(path)
        self.commands = commands or []
        self.pages_expresion = 'all'
        self._read_pdf_file = self._get_pdf_from_image(self.file_source.path)
        self._result_pages: list[PageObject] = self._read_pdf_file.pages

    def _get_pdf_from_image(self, source: Path) -> PdfReader:
        tmp_file_path = Path(self._TMP_PDF_NAME)
        image = Image.open(source)
        image.save(tmp_file_path)
        reader = PdfReader(tmp_file_path)
        tmp_file_path.unlink(missing_ok=True)
        return reader

    @property
    def reader(self) -> PdfReader:
        return self._read_pdf_file

    @property
    def last_result_pages(self) -> list[PageObject]:
        return self._result_pages

    @last_result_pages.setter
    def last_result_pages(self, pages: list[PageObject]) -> None:
        self._result_pages = pages

    @property
    def name(self) -> str:
        return self.file_source.path.name

    @cached_property
    def pages_count(self) -> int:
        return len(self.reader.pages)

    def __repr__(self) -> str:
        return f'<PdfSourceFromImage(name={self.name})>'
