from typing import TYPE_CHECKING
from pdf_toolkit.exceptions.invalid_pdf_command_type_error import InvalidPdfCommandTypeError
from . import PdfRotateCommand

if TYPE_CHECKING:
    from . import PdfCommand


class PdfCommandFactory:

    _MAPPING: dict[str, type['PdfCommand']] = {
        'rotate': PdfRotateCommand,
    }

    @classmethod
    def create_from_string(cls, command: str) -> 'PdfCommand':
        command_type, command_params = command.split(':', maxsplit=1)
        command_class = cls._MAPPING.get(command_type.lower())
        if command_class is None:
            raise InvalidPdfCommandTypeError(command_type)
        return command_class.create_from_string(command_params)
