import time
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

from pypdf import PageObject, PdfWriter


if TYPE_CHECKING:
    from pdf_toolkit.pdf_source import PdfSource


class PdfToolkit:
    def __init__(self, sources: list['PdfSource']) -> None:
        self._sources: list['PdfSource'] = sources

    @property
    def last_result_pages(self) -> list[PageObject]:
        return list(chain.from_iterable(source.last_result_pages for source in self._sources))

    def execute_commands(self) -> None:
        for source in self._sources:
            for command in source.commands:
                command.execute(source)

    def save_results(self, path: Path | str | None = None) -> None:
        writer = PdfWriter()
        for page in self.last_result_pages:
            writer.add_page(page)

        if path is None:
            path = Path(f'./pdf_output_{int(time.time())}.pdf')
        writer.write(Path(path))
