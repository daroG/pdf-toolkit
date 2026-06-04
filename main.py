from os import listdir
from os.path import isfile, join

from pypdf import PdfFileReader, PdfFileWriter

from pdf_toolkit.gui.main_window import app

pdf_source = 'Skan_Arkusz_Test_odp.pdf'


def rotate_pages(pdf_path: str, options: str):
    even = options in ['e', 'even', '2n']
    odd = options in ['o', 'odd', '2n+1']
    all = options in ['a', 'all', 'n']

    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(pdf_path)

    for i in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(i).rotateClockwise(180) if (
                even and i % 2 == 1 or odd and i % 2 == 0 or all) else pdf_reader.getPage(i)
        pdf_writer.addPage(page)

    f = pdf_path.split('\\')[-1].split('.pdf')[0]

    output_path = f"output/{f}_rotated.pdf"

    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)


# # ex: 1-5,7,9,12-16
# def decompose_pages_condition(conditions: str, max_number_of_pages: int):
#     separated_conditions = [s.strip() for s in conditions.split(',')]
#     pages = [(int(i) - 1) for i in separated_conditions if i.isnumeric() and int(i) <= max_number_of_pages]

#     for cond in [cond for cond in separated_conditions if not cond.isnumeric()]:
#         interval = cond.split('-')
#         if len(interval) != 2 or not (interval[0].isnumeric() and interval[1].isnumeric()):
#             raise Exception(f'Incorrect condition: {cond}')

#         start = int(interval[0]) - 1
#         end = int(interval[1]) - 1

#         if start >= end or end >= max_number_of_pages:
#             raise Exception(f'Incorrect condition: {cond}')

#         pages.extend(list(range(start, end+1)))

#     pages.sort()
#     return list(set(pages))


# def rotate_pages_different(pdf_path: str, pages: str):
#     pdf_writer = PdfFileWriter()
#     pdf_reader = PdfFileReader(pdf_path)

#     to_rotate = decompose_pages_condition(pages, pdf_reader.getNumPages())

#     for i in range(pdf_reader.getNumPages()):
#         page = pdf_reader.getPage(i).rotateClockwise(180) \
#             if i in to_rotate else pdf_reader.getPage(i)
#         pdf_writer.addPage(page)

#     f = pdf_path.split('\\')[-1].split('.pdf')[0]

#     output_path = f"output/{f}_rotated.pdf"

#     with open(output_path, 'wb') as fh:
#         pdf_writer.write(fh)


def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(output, 'wb') as out:
        pdf_writer.write(out)


def  main():

    # path = r'input\Rozdz4_tresc_rotated.pdf'
    # rotate_pages_different(path)

    to_merge_path = 'input/merge'

    # only_files_o = [f for f in listdir(odd_revers_path) if isfile(join(odd_revers_path, f))]
    # only_files_e = [f for f in listdir(even_revers_path) if isfile(join(even_revers_path, f))]

    # for f in only_files_o:
    #     rotate_pages(join(odd_revers_path, f), 'o')
    # for f in only_files_e:
    #     rotate_pages(join(even_revers_path, f), 'e')

    only_files_to_merge = [f for f in listdir(to_merge_path) if isfile(join(to_merge_path, f))]
    only_files_to_merge.sort()

    # print(only_files_to_merge)

    # rotate_pages_different(r'input\MatematykaDlaOpornych.pdf')

    # merge_pdfs([f"input/merge/{f}.pdf" for f in a_paths], 'output/MatematykaDlaOpornych.pdf')

    merge_pdfs([f"{to_merge_path}/{f}" for f in only_files_to_merge], 'output/dowod.pdf')
    # print("done")

    # print(decompose_pages_condition("1, 3, 6, 3-11, 22", 20))
    # merge_pdfs(['input/Dzial_10_zadania_1_rotated.pdf', 'input/Dzial_10_zadania_2_rotated.pdf'], 'output/Rozdz10_tresc_rotated')

if __name__ == '__main__':
    # main()
    app.mainloop()
