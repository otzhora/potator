from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict

from duplication.models import EntityData


@dataclass
class Index:
    lang: str
    l_depth: int
    tokens2entities: Dict[str, List[EntityData]]


def build_l_index(entities: List[EntityData], l_depth: int) -> Dict[str, Index]:
    tokens2entities = defaultdict(lambda: defaultdict(list))
    for entity in entities:
        lang = entity.object_data.lang
        tokens = entity.bag_of_tokens
        if len(tokens) > l_depth:
            tokens2entities[lang][tokens[l_depth]].append(entity)
    return {lang: Index(lang, l_depth, tokens2entities[lang]) for lang in tokens2entities.keys()}


class Indexer:
    def __init__(self, entities: List[EntityData], max_l_depth: int = 1):
        self.max_l_depth: int = max_l_depth

        self._indexes: List[Dict[str, Index]] = []

        for l_depth in range(1, self.max_l_depth + 1):
            self._indexes.append(build_l_index(entities, l_depth))

    def get_entities_for_token(self, token, lang, depth):
        return self._indexes[depth - 1][lang].tokens2entities[token]
