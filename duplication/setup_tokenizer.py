import os

from duplication.utils import *


def setup_tokenizer() -> None:
    """
    Clone GitHub repository with tokenizer and setup it.
    :return: None.
    """
    os.system(f'git clone {TOKENIZER_URL} {TOKENIZER_DIR}')
    os.chdir(TOKENIZER_DIR)
    os.system('git submodule update --init --recursive --depth 1')
    os.chdir('..')

    from .tokenizer.buckwheat.parsing import main
    os.chdir("tokenizer/buckwheat/parsing")
    main()


if __name__ == '__main__':
    setup_tokenizer()
