from collections.abc import Iterable
from os import listdir
from os.path import isfile, join
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_toolkit.gui.main_window import build_app


pdf_source = 'Skan_Arkusz_Test_odp.pdf'


def rotate_pages(pdf_path: str, options: str, output_path: str | None = None) -> str:
    even = options in ['e', 'even', '2n']
    odd = options in ['o', 'odd', '2n+1']
    rotate_all = options in ['a', 'all', 'n']

    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(pdf_path)

    for i, page in enumerate(pdf_reader.pages):
        if (even and i % 2 == 1) or (odd and i % 2 == 0) or rotate_all:
            page.rotate(180)
        pdf_writer.add_page(page)

    if output_path is None:
        output_path = f'output/{Path(pdf_path).stem}_rotated.pdf'

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with Path(output_path).open('wb') as fh:
        pdf_writer.write(fh)
    return output_path


def merge_pdfs(paths: Iterable[str], output: str) -> None:
    pdf_writer = PdfWriter()

    for path in paths:
        pdf_reader = PdfReader(path)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with Path(output).open('wb') as out:
        pdf_writer.write(out)


def main() -> None:
    to_merge_path = 'input/merge'

    only_files_to_merge = [f for f in listdir(to_merge_path) if isfile(join(to_merge_path, f))]
    only_files_to_merge.sort()

    merge_pdfs([f'{to_merge_path}/{f}' for f in only_files_to_merge], 'output/dowod.pdf')


if __name__ == '__main__':
    build_app().mainloop()
