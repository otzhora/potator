from duplication.extractors import EntitiesExtractor
from duplication.indexer import Indexer, get_tokens_bounds
from duplication.models import CloneData, DetectionResult, EntityData
from duplication.similarity_metrics import jaccard
from duplication.utils import sort_tokens_gtc


def _validate_entity_candidate(entity: EntityData, candidate: EntityData) -> bool:
    return hash(entity) != hash(candidate) and entity.object_data.lang == candidate.object_data.lang and \
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

                # TODO: token position filtering
                sim = jaccard(entity.bag_of_tokens, candidate.bag_of_tokens)
                if sim > threshold:
                    clones.append(CloneData(entity, candidate, sim))

        clones = list(sorted(clones, reverse=True))

        return DetectionResult(clones, f"NaiveDetector(), directory: {directory}, threshold: {threshold}, "
                                       f"granularity: {granularity}")


class FilteringDetector(Detector):
    def __init__(self, max_l_depth: int = 1):
        self.max_l_depth = max_l_depth

    def detect(self, directory: str, threshold: float, granularity: str) -> DetectionResult:
        files, files_data, entities = EntitiesExtractor.extract_data_from_directory(directory, granularity)
        sort_tokens_gtc(entities)
        indexer = Indexer(entities, self.max_l_depth, threshold)

        clones = []
        considered_pairs = set()
        for i in range(len(entities)):
            entity = entities[i]
            lang = entity.object_data.lang
            tokens = entity.bag_of_tokens

            candidates = set()
            for l_depth in range(1, self.max_l_depth + 1):
                left_bound, right_bound = get_tokens_bounds(tokens, l_depth, threshold)
                for token in tokens[left_bound: right_bound]:
                    candidates.update(indexer.get_entities_for_token(token, lang, l_depth))

            for candidate in candidates:
                if not _validate_entity_candidate(entity, candidate):
                    continue
                if (entity, candidate) in considered_pairs or (candidate, entity) in considered_pairs:
                    continue

                sim = jaccard(entity.bag_of_tokens, candidate.bag_of_tokens)
                if sim > threshold:
                    clones.append(CloneData(entity, candidate, sim))
                    considered_pairs.add((entity, candidate))

        clones = list(sorted(clones, reverse=True))

        return DetectionResult(clones, f"FilteringDetector({self.max_l_depth}), directory: {directory}, "
                                       f"threshold: {threshold}, granularity: {granularity}")
