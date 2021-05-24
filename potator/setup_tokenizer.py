import os
from pathlib import Path


TOKENIZER_DIR = 'potator/tokenizer'
TOKENIZER_URL = 'https://github.com/otzhora/buckwheat'


def setup_tokenizer() -> None:
    """
    Clone GitHub repository with tokenizer and setup it.
    :return: None.
    """
    cwd = Path(os.getcwd())

    if not os.path.exists(cwd/TOKENIZER_DIR):
        os.system(f'git clone {TOKENIZER_URL} {TOKENIZER_DIR}')

    os.chdir(cwd/TOKENIZER_DIR)
    os.system(f'git pull')
    os.system('git submodule update --init --recursive --depth 1')
    os.chdir('..')

    from .tokenizer.buckwheat.parsing import main as parsing_main
    os.chdir(cwd/TOKENIZER_DIR/"buckwheat"/"parsing")
    parsing_main()

    from .tokenizer.buckwheat.language_recognition import main as enry_main
    os.chdir(cwd/TOKENIZER_DIR/"buckwheat"/"language_recognition")
    enry_main()
    os.chdir(cwd)


if __name__ == '__main__':
    setup_tokenizer()
