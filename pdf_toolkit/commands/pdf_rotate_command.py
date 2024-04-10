from typing import Any, Self

from pypdf import PageObject

from pdf_toolkit.pdf_toolkit import PdfSource
from . import PdfCommand


class PdfRotateCommand(PdfCommand):
    def __init__(self, pages: str, angle: str | int) -> None:
        self._pages: list[int] = self.translate_pages_string(pages)
        self._angle = int(angle)

    @classmethod
    def create_from_string(cls, params: str) -> Self:
        pages, angle = params.split('|', maxsplit=1)
        return cls(pages, angle)

    def execute(self, source: PdfSource) -> list[PageObject]:
        new_pages = []
        for idx, page in enumerate(source.last_result_pages, 1):
            if idx in self._pages:
                new_pages.append(page.rotate(self._angle))
            else:
                new_pages.append(page)

        return new_pages
