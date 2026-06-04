from .pdf_toolkit_exception import PdfToolkitError


class InvalidPageConditionError(PdfToolkitError):
    def __init__(self, condition: str) -> None:
        super().__init__(f'Invalid page condition: "{condition}".')
