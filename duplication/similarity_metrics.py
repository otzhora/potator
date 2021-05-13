from typing import List


def overlap(bag_of_tokens1: List[str], bag_of_tokens2: List[str]) -> float:
    """
    Given two bag of tokens return their overlap
    :param bag_of_tokens1:
    :param bag_of_tokens2:
    :return: value of overlap
    """
    return sum(token1 in bag_of_tokens2 for token1 in bag_of_tokens1)


def jaccard(bag_of_tokens1: List[str], bag_of_tokens2: List[str]) -> float:
    """
    Given two bag of tokens return their jaccard similarity
    :param bag_of_tokens1:
    :param bag_of_tokens2:
    :return: value of overlap
    """
    return overlap(bag_of_tokens1, bag_of_tokens2) / max(len(bag_of_tokens1), len(bag_of_tokens2))