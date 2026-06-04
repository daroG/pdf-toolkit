import argparse
from pathlib import Path

from pdf_toolkit.image_optimizer.jpg_optimizer import JpgOptimizer


def optimize_directory(input_path: str | Path, output_path: str | Path) -> int:
    """
    Optimize every image file in ``input_path`` into ``output_path``.

    :param input_path: directory containing source images
    :param output_path: directory to write optimized images into
    :return: number of images optimized
    """
    input_dir = Path(input_path)
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    images = sorted(path for path in input_dir.iterdir() if path.is_file())
    for image in images:
        optimized = JpgOptimizer.load_from_path(image).optimize()
        (output_dir / image.name).write_bytes(optimized)

    return len(images)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description='Optimize JPEG images with guetzli.')
    parser.add_argument('input', help='directory containing source images')
    parser.add_argument('output', help='directory to write optimized images into')
    args = parser.parse_args(argv)

    count = optimize_directory(args.input, args.output)
    print(f'Optimized {count} images')


if __name__ == '__main__':
    main()
