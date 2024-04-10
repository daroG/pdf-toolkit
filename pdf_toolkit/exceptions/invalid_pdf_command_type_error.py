from .pdf_toolkit_exception import PdfToolkitError


class InvalidPdfCommandTypeError(PdfToolkitError):
    def __init__(self, command_type: str) -> None:
        super().__init__(f'Given command type "{command_type}" is not a valid command type.')
