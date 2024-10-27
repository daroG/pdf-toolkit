from enum import StrEnum

from pdf_toolkit.exceptions.invalid_page_condition_exception import InvalidPageConditionError


class PageNumberComparator:
    """
    Page number comparator.
    """

    class PageNumbersFormatType(StrEnum):
        """Page number format type."""

        #: 1, 3, 5 ...
        ODD = 'odd'
        #: 2, 4, 6 ...
        EVEN = 'even'
        ALL = 'all'
        NUMERAL = 'numeral'

    def __init__(self, pages: str) -> None:
        self.pages_format = self._detect_page_string_type(pages)
        self._pages = self._calculate_pages(pages)

    def _detect_page_string_type(self, pages: str) -> PageNumbersFormatType:
        pages = pages.strip().lower()
        if pages == 'odd':
            return self.PageNumbersFormatType.ODD
        if pages == 'even':
            return self.PageNumbersFormatType.EVEN
        if pages == 'all':
            return self.PageNumbersFormatType.ALL

        return self.PageNumbersFormatType.NUMERAL

    def _calculate_pages(self, pages: str) -> set[int] | None:
        if self.pages_format is not self.PageNumbersFormatType.NUMERAL:
            return None
        return self._translate_pages_string(pages)

    def is_page_in_range(self, page_id: int) -> bool:
        """
        Validate if given page_id (counted from 0) is in the range.

        :param page_id: page no
        :return: bool
        """
        match self.pages_format:
            case self.PageNumbersFormatType.ALL:
                return True
            case self.PageNumbersFormatType.ODD:
                #: need to reverse logic when comparing, because given page id is counted from 0 not from 1
                return page_id % 2 == 0
            case self.PageNumbersFormatType.EVEN:
                #: need to reverse logic when comparing, because given page id is counted from 0 not from 1
                return page_id % 2 == 1
            case self.PageNumbersFormatType.NUMERAL:
                return page_id in self._pages
        return False

    @classmethod
    def _translate_pages_string(cls, pages_string: str, max_number_of_pages: int = -1) -> set[int]:
        """
        Translate given pages string into list of integers representing indexes of pages.

        :param pages_string: pages numbers in string
        :param max_number_of_pages: maximum number of pages, defaults to -1
        :return: set of pages indexes
        """
        numeric_conditions, non_numeric = cls._get_separated_conditions(pages_string)
        if max_number_of_pages < 0:
            max_number_of_pages = 2**32
        pages = {
            (page_number - 1) for page_number in numeric_conditions if page_number <= max_number_of_pages
        }
        for cond in non_numeric:
            if '-' not in cond:
                raise InvalidPageConditionError(cond)
            cond_start, _, cond_end = cond.partition('-')
            try:
                start = int(cond_start) - 1
                end = int(cond_end) - 1
            except ValueError:
                raise InvalidPageConditionError(cond) from None

            if start >= end or end >= max_number_of_pages:
                raise InvalidPageConditionError(cond)

            pages.update(range(start, end + 1))
        return pages

    @staticmethod
    def _get_separated_conditions(pages_string: str) -> tuple[list[int], list[str]]:
        numeric, non_numeric = [], []
        for condition in pages_string.split(','):
            striped_condition = condition.strip()
            if striped_condition.isnumeric():
                numeric.append(int(striped_condition))
            else:
                non_numeric.append(striped_condition)
        return numeric, non_numeric
