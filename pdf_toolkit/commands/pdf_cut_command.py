from typing import Self

from pdf_toolkit.commands.pdf_command import PdfCommand
from pdf_toolkit.pdf_toolkit import PdfSource


class PdfCutCommand(PdfCommand):

    def __init__(self, pages: str) -> None:
        self._pages = self.translate_pages_string(pages)

    @classmethod
    def create_from_string(cls, params: str) -> Self:
        return cls(params)

    def execute(self, source: PdfSource) -> None:
        source.last_result_pages = [source.last_result_pages[i - 1] for i in self._pages]
