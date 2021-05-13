import os


TOKENIZER_DIR = 'duplication/tokenizer'
TOKENIZER_URL = 'https://github.com/otzhora/buckwheat'


def mkdir(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.isdir(path):
        raise ValueError(f'{path} is not a directory!')

