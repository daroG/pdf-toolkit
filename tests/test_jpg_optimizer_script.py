from pathlib import Path

from PIL import Image


def _write_jpeg(path: Path) -> None:
    Image.new('RGB', (32, 32), color='red').save(path, format='JPEG')


def test_optimize_directory_writes_every_image(tmp_path: Path):
    import jpgOptimizer

    in_dir = tmp_path / 'in'
    out_dir = tmp_path / 'out'
    in_dir.mkdir()
    _write_jpeg(in_dir / 'one.jpg')
    _write_jpeg(in_dir / 'two.jpg')

    count = jpgOptimizer.optimize_directory(str(in_dir), str(out_dir))

    assert count == 2
    assert (out_dir / 'one.jpg').read_bytes()
    assert (out_dir / 'two.jpg').read_bytes()
