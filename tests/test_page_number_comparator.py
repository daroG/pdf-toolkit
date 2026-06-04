import pytest

from pdf_toolkit.exceptions import InvalidPageConditionError
from pdf_toolkit.page_number_comparator import PageNumberComparator


@pytest.mark.parametrize(
    ['input_value', 'expected_pages'],
    [
        ('1,2,3,4', {0, 1, 2, 3}),
        ('1-4', {0, 1, 2, 3}),
        ('1,2,5-7,8-10', {0, 1, 4, 5, 6, 7, 8, 9}),
        (' 1 ,   2, 5 - 7, 8-10', {0, 1, 4, 5, 6, 7, 8, 9}),
        ('1-10,5-7,8-10, 3, 2, 1', {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}),
    ],
)
def test_translate_pages_string(input_value: str, expected_pages: set[int]):
    assert PageNumberComparator._translate_pages_string(input_value) == expected_pages


def test_single_page_within_max_is_kept():
    assert PageNumberComparator._translate_pages_string('3', max_number_of_pages=3) == {2}


def test_single_page_beyond_max_raises():
    # A single out-of-range page must raise, consistently with how ranges are validated.
    with pytest.raises(InvalidPageConditionError):
        PageNumberComparator._translate_pages_string('5', max_number_of_pages=3)


def test_range_beyond_max_raises():
    with pytest.raises(InvalidPageConditionError):
        PageNumberComparator._translate_pages_string('1-5', max_number_of_pages=3)
