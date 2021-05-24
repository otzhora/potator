from collections import Counter
from typing import List


def overlap(bag_of_tokens1: List[str], bag_of_tokens2: List[str]) -> float:
    """
    Given two bag of tokens return their overlap
    :param bag_of_tokens1:
    :param bag_of_tokens2:
    :return: value of overlap
    """
    return sum((Counter(bag_of_tokens1) & Counter(bag_of_tokens2)).values())


def jaccard(bag_of_tokens1: List[str], bag_of_tokens2: List[str]) -> float:
    """
    Given two bag of tokens return their jaccard similarity
    :param bag_of_tokens1:
    :param bag_of_tokens2:
    :return: value of overlap
    """
    max_len = max(len(bag_of_tokens1), len(bag_of_tokens2))
    if max_len == 0:
        return 0
    return overlap(bag_of_tokens1, bag_of_tokens2) / max_len
