from setuptools import setup
from os import path
import pathlib

from potator.setup_tokenizer import setup_tokenizer


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

with open(HERE / 'requirements.txt', 'r', encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
    install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (not x.startswith('#'))
                        and (not x.startswith('-'))]
    dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup_tokenizer()

setup(
    name='potator',
    description='',
    version='0.1.1',
    packages=['potator'],
    package_dir={'potator': 'potator'},
    install_requires=install_requires,
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
    download_url='https://github.com/otzhora/potator/releases/tag/v0.1.1',
    dependency_links=dependency_links,
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
        'Programming Language :: Python :: 3.8'])
