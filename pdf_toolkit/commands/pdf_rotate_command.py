from typing import Self, TYPE_CHECKING

from pdf_toolkit.commands.pdf_command import PdfCommand
from pdf_toolkit.page_number_comparator import PageNumberComparator


if TYPE_CHECKING:
    from pdf_toolkit.pdf_toolkit import PdfSource


class PdfRotateCommand(PdfCommand):
    """
    Pdf Command for rotating the source pages.
    """

    def __init__(self, pages: str, angle: str | int) -> None:
        self._page_number_comparator = PageNumberComparator(pages)
        self._angle = int(angle)

    @classmethod
    def create_from_string(cls, params: str) -> Self:
        """
        Create instance of the command of string params.

        :param params: stringified parameters
        :return: instance of the command
        """
        pages, angle = params.split('|', maxsplit=1)
        return cls(pages, angle)

    def execute(self, source: 'PdfSource') -> None:
        """
        Execute command on given source.

        :param source: PdfSource
        """
        new_pages = []
        for idx, page in enumerate(source.last_result_pages):
            if self._page_number_comparator.is_page_in_range(idx):
                new_pages.append(page.rotate(self._angle))
            else:
                new_pages.append(page)

        source.last_result_pages = new_pages
