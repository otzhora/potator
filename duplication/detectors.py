from duplication.extractors import EntitiesExtractor
from duplication.models import CloneData, DetectionResult, EntityData
from duplication.similarity_metrics import jaccard
from duplication.utils import sort_tokens_gtc


def _validate_entity_candidate(entity: EntityData, candidate: EntityData) -> bool:
    return entity != candidate and entity.object_data.lang == candidate.object_data.lang and \
           entity.object_data.object_type == candidate.object_data.object_type


class Detector:
    def detect(self, directory: str, threshold: float, granularity: str) -> DetectionResult:
        raise NotImplemented


class NaiveDetector(Detector):
    def detect(self, directory: str, threshold: float, granularity: str) -> DetectionResult:
        files, files_data, entities = EntitiesExtractor.extract_data_from_directory(directory, granularity)

        clones = []
        for i in range(len(entities)):
            entity = entities[i]
            for j in range(i + 1, len(entities)):
                candidate = entities[j]
                if not _validate_entity_candidate(entity, candidate):
                    continue

                sim = jaccard(entity.bag_of_tokens, candidate.bag_of_tokens)
                if sim > threshold:
                    clones.append(CloneData(entity, candidate, sim))

        clones = list(sorted(clones, reverse=True))

        return DetectionResult(clones, f"NaiveDetector(), directory: {directory}, threshold: {threshold}, "
                                       f"granularity: {granularity}")


class FilteringDetector(Detector):
    def detect(self, directory: str, threshold: float, granularity: str) -> DetectionResult:
        files, files_data, entities = EntitiesExtractor.extract_data_from_directory(directory, granularity)
        sort_tokens_gtc(entities)

        return DetectionResult([], f"FilteringDetector(), directory: {directory}, threshold: {threshold}, "
                                   f"granularity: {granularity}")
