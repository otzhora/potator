from collections import defaultdict
from dataclasses import dataclass
from math import ceil
from typing import List, Dict, Tuple

from potator.models import EntityData


@dataclass
class Index:
    lang: str
    l_depth: int
    tokens2entities: Dict[str, List[EntityData]]


def get_tokens_bounds(tokens: List[str], l_depth: int, thr: float) -> Tuple[int, int]:
    left_bound = 0 if l_depth == 1 else len(tokens) - ceil(thr * len(tokens)) + l_depth - 1
    right_bound = len(tokens) - ceil(thr * len(tokens)) + l_depth
    return left_bound, right_bound


# TODO: maybe bounds should be on number of unique tokens. Think about that
def build_l_index(entities: List[EntityData], l_depth: int, thr: float = 0.8) -> Dict[str, Index]:
    tokens2entities = defaultdict(lambda: defaultdict(list))
    for entity in entities:
        lang = entity.object_data.lang
        tokens = entity.bag_of_tokens

        left_bound, right_bound = get_tokens_bounds(tokens, l_depth, thr)

        for token in set(tokens[left_bound: right_bound]):
            tokens2entities[lang][token].append(entity)

    return {lang: Index(lang, l_depth, tokens2entities[lang]) for lang in tokens2entities.keys()}


class Indexer:
    def __init__(self, entities: List[EntityData], max_l_depth: int = 1, threshold: float = 0.8):
        self.max_l_depth: int = max_l_depth
        self.threshold: float = threshold

        self._indexes: List[Dict[str, Index]] = []

        for l_depth in range(1, self.max_l_depth + 1):
            self._indexes.append(build_l_index(entities, l_depth, self.threshold))

    def get_entities_for_token(self, token, lang, depth):
        return self._indexes[depth - 1][lang].tokens2entities[token]
