from abc import ABC, abstractmethod
from typing import Self, TYPE_CHECKING


if TYPE_CHECKING:
    from pdf_toolkit.pdf_source import PdfSource


class PdfCommand(ABC):
    """
    Pdf Command base.
    """

    @classmethod
    @abstractmethod
    def create_from_string(cls, params: str) -> Self:
        """Create command instance from given string params."""

    @abstractmethod
    def execute(self, source: 'PdfSource') -> None:
        """Execute the command."""
