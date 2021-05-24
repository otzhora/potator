from dataclasses import dataclass
from typing import List, Tuple

from potator.tokenizer.buckwheat.utils import ObjectData


File = Tuple[str, str]


@dataclass
class EntityData:
    object_data: ObjectData
    bag_of_tokens: List[str]
    file_path: str

    def __hash__(self):
        return hash(f"{self.file_path} + {self.object_data.content}")


@dataclass
class CloneData:
    entity_1: EntityData
    entity_2: EntityData
    similarity: float

    def __lt__(self, other):
        return self.similarity < other.similarity


@dataclass
class DetectionResult:
    """
    Class for storing results of detection
    """
    clones: List[CloneData]
    used_algorithm: str
