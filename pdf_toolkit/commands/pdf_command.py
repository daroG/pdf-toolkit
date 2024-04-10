from abc import ABC, abstractmethod
from typing import Self

from pypdf import PageObject

from pdf_toolkit.exceptions import InvalidPageConditionError
from pdf_toolkit.pdf_toolkit import PdfSource

class PdfCommand(ABC):
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

    @classmethod
    def translate_pages_string(cls, pages_string: str, max_number_of_pages: int = -1) -> list[int]:
        numeric_conditions, non_numeric = cls._get_separated_conditions(pages_string)
        if max_number_of_pages < 0:
            max_number_of_pages = 2**32
        pages = set(
            (page_number - 1) for page_number in numeric_conditions if page_number <= max_number_of_pages
        )
        for cond in non_numeric:
            if '-' not in cond:
                raise InvalidPageConditionError(cond)
            cond_start, _, cond_end = cond.partition('-')
            try:
                start = int(cond_start) - 1
                end = int(cond_end) - 1
            except ValueError:
                raise InvalidPageConditionError(cond)

            if start >= end or end >= max_number_of_pages:
                raise InvalidPageConditionError(cond)

            pages.update(range(start, end+1))
        return sorted(list(pages))

    @classmethod
    @abstractmethod
    def create_from_string(cls, params: str) -> Self:
        """Create command instance from given string params."""

    @abstractmethod
    def execute(self, source: PdfSource) -> None:
        """Execute a command"""
