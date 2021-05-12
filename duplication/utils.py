import os
from pathlib import Path


TOKENIZER_DIR = Path('tokenizer')
TOKENIZER_URL = 'https://github.com/JetBrains-Research/identifiers-extractor.git'
TOKENIZER_VERSION = 'v1.1.1'


def mkdir(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.isdir(path):
        raise ValueError(f'{path} is not a directory!')

