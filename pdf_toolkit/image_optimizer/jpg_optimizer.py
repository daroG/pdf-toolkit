from pathlib import Path

import pyguetzli


class JpgOptimizer:
    def __init__(self, image: bytes) -> None:
        self._image = image

    @classmethod
    def load_from_path(cls, path: str | Path) -> 'JpgOptimizer':
        path = Path(path)
        return cls(path.read_bytes())

    def optimize(self) -> bytes:
        return pyguetzli.process_jpeg_bytes(self._image)
