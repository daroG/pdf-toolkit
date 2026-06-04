from typing import TYPE_CHECKING

from pdf_toolkit.commands import PdfCutCommand, PdfRotateCommand
from pdf_toolkit.exceptions.invalid_pdf_command_type_error import InvalidPdfCommandTypeError


if TYPE_CHECKING:
    from pdf_toolkit.commands import PdfCommand


_COMMAND_TYPE_SEPARATOR: str = ':'


class PdfCommandFactory:
    """
    Pdf Command factory.
    """

    _MAPPING: dict[str, type['PdfCommand']] = {
        'cut': PdfCutCommand,
        'rotate': PdfRotateCommand,
    }

    @classmethod
    def create_from_string(cls, command: str) -> 'PdfCommand':
        """
        Create a command from given command string.

        :param command: stringified PdfCommand
        :return: instance of PdfCommand
        """
        command_type, command_params = command.split(_COMMAND_TYPE_SEPARATOR, maxsplit=1)
        command_class = cls._MAPPING.get(command_type.lower())
        if command_class is None:
            raise InvalidPdfCommandTypeError(command_type)
        return command_class.create_from_string(command_params)
