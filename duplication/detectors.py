import functools
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

from duplication.similarity_metrics import jaccard
from duplication.tokenizer.buckwheat import recognize_languages_dir
from duplication.tokenizer.buckwheat.tokenizer import get_data_from_file, get_identifiers_sequence_from_code
from duplication.tokenizer.buckwheat.utils import FileData, transform_files_list, get_full_path, ObjectTypes, ObjectData


class EntityTypes(Enum):
    Function = 0
    Class = 1


@dataclass
class EntityData:
    entity_type: EntityTypes
    path: str
    lang: str
    bag_of_tokens: List[str]


@dataclass
class DetectionResult:
    """
    Class for storing results of detection
    """
    clones: List[Tuple[EntityData, EntityData, float]]


File = Tuple[str, str]


class Detector:
    def __init__(self):
        self.files: List[str] = []
        self.files_data: List[FileData] = []
        self.entities: List[EntityData] = []

    @staticmethod
    def extract_entity_from_object_data(obj: ObjectData, path, lang) -> EntityData:
        entity_type = ""
        if obj.object_type == ObjectTypes.FUNCTION:
            entity_type = EntityTypes.Function
        if obj.object_type == ObjectTypes.CLASS:
            entity_type = EntityTypes.Class

        entity_tokens = get_identifiers_sequence_from_code(obj.content, lang)
        return EntityData(entity_type, path, lang, entity_tokens)

    @staticmethod
    def extract_entity_from_file_data(file: FileData) -> List[EntityData]:
        entity_path = file.path
        entity_lang = file.lang
        return [Detector.extract_entity_from_object_data(obj, entity_path, entity_lang) for obj in file.objects]

    @staticmethod
    def extract_entities_from_files_data(files: List[FileData]) -> List[EntityData]:
        def acc(value: List[EntityData], file_data: FileData) -> List[EntityData]:
            value.extend(Detector.extract_entity_from_file_data(file_data))
            return value

        return functools.reduce(acc, files, [])

    @staticmethod
    def extract_data_from_files(files: List[File]) -> List[FileData]:
        return [get_data_from_file(file, lang, True, False) for file, lang in files]

    def fill_fields(self, directory: str, granularity: str):
        lang2files = recognize_languages_dir(directory)
        files = transform_files_list(lang2files, granularity, None)
        self.files = [(get_full_path(file, directory), lang) for file, lang in files]
        self.files_data = self.extract_data_from_files(self.files)
        self.entities = self.extract_entities_from_files_data(self.files_data)

    def detect(self, directory: str, threshold: float, granularity: str) -> List[DetectionResult]:
        raise NotImplemented


class NaiveDetector(Detector):
    def detect(self, directory: str, threshold: float, granularity: str) -> DetectionResult:
        self.fill_fields(directory, granularity)
        clones = []
        for i in range(len(self.entities)):
            entity = self.entities[i]
            for j in range(i + 1, len(self.entities)):
                candidate = self.entities[j]
                if entity == candidate or entity.lang != candidate.lang:
                    continue

                sim = jaccard(entity.bag_of_tokens, candidate.bag_of_tokens)
                if sim > threshold:
                    clones.append((entity, candidate, sim))
        return DetectionResult(clones)
