from setuptools import setup
from os import path
import pathlib

from duplication.setup_tokenizer import setup_tokenizer


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
    install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (not x.startswith('#'))
                        and (not x.startswith('-'))]
    dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup_tokenizer()

setup(
    name='code_duplication_detector',
    description='',
    version='0.1.0',
    packages=['code_duplication_detector'],
    package_dir={'code_duplication_detector': 'code-duplication-detector'},
    install_requires=install_requires,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'code_duplication_detector = code-duplication-detector.__main__:main'
        ]
    },
    author="Yuriy Rogachev",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/otzhora/code_duplication_detector',
    download_url='https://github.com/otzhora/code_duplication_detector/releases/tag/v0.1.0',
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
