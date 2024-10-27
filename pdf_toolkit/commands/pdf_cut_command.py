from typing import Self, TYPE_CHECKING

from pdf_toolkit.commands.pdf_command import PdfCommand
from pdf_toolkit.page_number_comparator import PageNumberComparator
from pdf_toolkit.source_page_iterator import SourcePagesIterator


if TYPE_CHECKING:
    from pdf_toolkit.pdf_toolkit import PdfSource


class PdfCutCommand(PdfCommand):
    """
    Pdf Command for cutting the source.
    """

    def __init__(self, pages: str) -> None:
        self._page_comparator = PageNumberComparator(pages)

    @classmethod
    def create_from_string(cls, params: str) -> Self:
        """
        Create instance of the command of string params.

        :param params: stringified parameters
        :return: instance of the command
        """
        return cls(params)

    def execute(self, source: 'PdfSource') -> None:
        """
        Execute command on given source.

        :param source: PdfSource
        """
        source.last_result_pages = list(iter(SourcePagesIterator(self._page_comparator, source)))
