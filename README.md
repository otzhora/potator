Small code clone detection tool. It implements an algorithm from [SourcererCC](https://arxiv.org/abs/1512.06448) with [adaptive prefix filtering](https://www.sciencedirect.com/science/article/abs/pii/S0164121217302790) optimizations and displays its results as HTML. 

# Supported platforms

`potator` supports Linux and macOS. It is possible to use `potator` on Windows under WSL

# Installation

## Using pip

`potator` can be installed using pip

```bash
pip install potator
```

## Using installation script

```bash
git clone https://github.com/otzhora/potator
cd potator
./install.sh
```

# Usage

## Using `potator` as a standalone cli application

```bash
potator [-h] [-d {Naive,Filtering}] [--depth DEPTH] [-t THRESHOLD] [-g GRANULARITY] [-o OUT] directory 
```

### Options

* You can choose one of two detectors: Naive and Filtering. Naive detector compares every possible combination of source code fragments and calculates jaccard similarity between them. Filtering detector implements algorithm from SourcererCC paper with an adaptive prefix filtering optimizations.
* Depth parameters specify the maximum depth of adaptive prefix. `depth=2` is recommended. Since it offers the optimal balance between costs of building index and querying it. 
* Threshold is the minimum score that two code fragments should have to be considered clones.
* Granularity specifies granularity of code blocks. Options are `functions` and `classes`. `functions` is recommended.
* Out specifies the name of the resulting html
* Directory is the directory with files on which to perform search.

You can also do `export DEBUG=1` before the search, then profiling information will be printed out.

## Using `potator` as python package

You can import detectors or entities extractor from `potator` and use them to work with source code.

```python
>>> from potator.detectors import FilteringDetector
>>> detector = FilteringDetector()
>>> detector.detect(directory, thershold, granularity)
```

```python
>>> from potator.extractors import EntitiesExtractor
>>> EntitiesExtractor.extract_data_from_directory(directory, granularity)
```
