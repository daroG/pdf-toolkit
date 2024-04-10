from dataclasses import dataclass


@dataclass
class CliApp:
    file_path: str


app = CliApp()
def load_file():
    print('File loading')
    app.file_path = input('Enter the file path:')
