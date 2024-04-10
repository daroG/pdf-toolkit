
import pytest
from pdf_toolkit.commands.pdf_command import PdfCommand


@pytest.mark.parametrize(
    ['input', 'expected_pages'],
    [
        ('1,2,3,4', [0, 1, 2, 3]),
        ('1-4', [0, 1, 2, 3]),
        ('1,2,5-7,8-10', [0, 1, 4, 5, 6, 7, 8, 9]),
        (' 1 ,   2, 5 - 7, 8-10', [0, 1, 4, 5, 6, 7, 8, 9]),
        ('1-10,5-7,8-10, 3, 2, 1', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ],
)
def test_translate_pages_string(input: str, expected_pages: list[int]):
    assert PdfCommand.translate_pages_string(input) == expected_pages
