from __future__ import annotations

from pathlib import Path
from typing import List

from PIL import Image


def load_images(paths: List[Path]) -> List[Image.Image]:
    return [Image.open(path) for path in paths]
