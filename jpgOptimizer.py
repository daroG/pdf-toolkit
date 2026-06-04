from os import listdir
from os.path import isfile, join

import pyguetzli


if __name__ == '__main__':

    input_path = 'D:/Obrazy/wanda&darek/2. ceremonia'
    output_path = 'D:/Obrazy/wanda&darek/2. ceremonia - optimized'

    only_files = [f for f in listdir(input_path) if isfile(join(input_path, f))]

    print(f"Read {len(only_files)} images")

    for f in only_files:
        print(f"{f} in progress")
        input_jpeg = open(join(input_path, f), "rb").read()
        print(f"{f} opened")
        optimized_jpeg = pyguetzli.process_jpeg_bytes(input_jpeg)
        print(f"{f} optimized")

        output = open(join(output_path, f), "wb")
        print(f"{f} trying to write")
        output.write(optimized_jpeg)
        print(f"{f} - done")
