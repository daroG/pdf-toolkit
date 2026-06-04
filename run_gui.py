import logging

from pdf_toolkit.gui.main_window import build_app


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    build_app().mainloop()
