from dataclasses import dataclass
from typing import List, Tuple

from duplication.tokenizer.buckwheat.utils import ObjectData


@dataclass
class EntityData:
    object_data: ObjectData
    bag_of_tokens: List[str]
    file_path: str


@dataclass
class DetectionResult:
    """
    Class for storing results of detection
    """
    clones: List[Tuple[EntityData, EntityData, float]]


File = Tuple[str, str]
