from collections.abc import Callable
from pathlib import Path

from pypdf import PdfReader


def test_merge_pdfs_combines_all_pages(make_pdf: Callable[..., Path], tmp_path: Path):
    import main

    first = make_pdf(2, 'a.pdf')
    second = make_pdf(3, 'b.pdf')
    out = tmp_path / 'merged.pdf'

    main.merge_pdfs([str(first), str(second)], str(out))

    assert len(PdfReader(str(out)).pages) == 5


def test_rotate_pages_rotates_every_page_for_all_option(
    make_pdf: Callable[..., Path], tmp_path: Path
):
    import main

    src = make_pdf(2, 'src.pdf')
    out = tmp_path / 'rotated.pdf'

    main.rotate_pages(str(src), 'all', str(out))

    assert [page.rotation for page in PdfReader(str(out)).pages] == [180, 180]


def test_rotate_pages_only_rotates_even_pages(
    make_pdf: Callable[..., Path], tmp_path: Path
):
    import main

    src = make_pdf(4, 'src.pdf')
    out = tmp_path / 'rotated.pdf'

    main.rotate_pages(str(src), 'even', str(out))

    # 'even' rotates 1-based even pages -> 0-based odd indices.
    assert [page.rotation for page in PdfReader(str(out)).pages] == [0, 180, 0, 180]
