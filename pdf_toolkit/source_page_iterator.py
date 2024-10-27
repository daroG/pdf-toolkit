from typing import Self, TYPE_CHECKING

from pypdf import PageObject

from pdf_toolkit.page_number_comparator import PageNumberComparator


if TYPE_CHECKING:
    from pdf_toolkit.pdf_toolkit import PdfSource


class SourcePagesIterator:
    def __init__(self, page_comparator: PageNumberComparator, source: 'PdfSource') -> None:
        self._page_comparator = page_comparator
        self._source = source
        self._max_iter = len(source.reader.pages)

    def __iter__(self) -> Self:
        self._last_page_index = -1
        return self

    def __next__(self) -> PageObject:
        for next_page_index in range(self._last_page_index + 1, self._max_iter):
            if self._page_comparator.is_page_in_range(next_page_index):
                break
        else:
            raise StopIteration
        try:
            self._last_page_index = next_page_index
            return self._source.reader.pages[next_page_index]
        except IndexError:
            raise StopIteration from None
