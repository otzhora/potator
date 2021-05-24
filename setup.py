from setuptools import setup

from duplication.setup_tokenizer import setup_tokenizer


setup_tokenizer()

setup(
    name='duplication',
    version='0.1.0',
    packages=['duplication'],
    entry_points={
        'console_scripts': [
            'duplication = duplication.__main__:main'
        ]
    })
