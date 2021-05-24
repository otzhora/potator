from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import pathlib

from potator.setup_tokenizer import setup_tokenizer


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        setup_tokenizer()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        setup_tokenizer()


setup(
    name='potator',
    description='',
    version='0.1.2',
    packages=['potator'],
    package_dir={'potator': 'potator'},
    install_requires=[
        'pygments',
        'joblib',
        'tqdm',
        'tree_sitter',
        'PyStemmer',
        'Cython'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'potator = potator.__main__:main'
        ]
    },
    author="Yuriy Rogachev",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/otzhora/potator',
    download_url='https://github.com/otzhora/potator/releases/tag/v0.1.2',
    keywords=['STATIC-ANALYSIS', 'PLAGIARISM-DETECTION', 'PLAGIARISM-DETECTOR'],
    author_email='rogachev.yuiry28@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
    })
