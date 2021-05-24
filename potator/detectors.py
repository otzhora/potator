from dataclasses import dataclass
from math import ceil
from typing import List

from potator.extractors import EntitiesExtractor
from potator.indexer import Indexer, get_tokens_bounds
from potator.models import CloneData, DetectionResult, EntityData
from potator.similarity_metrics import jaccard
from potator.utils import sort_tokens_gtc, LANGUAGE_ORDER
from potator.profiler import Profile


def _validate_entity_candidate(entity: EntityData, candidate: EntityData) -> bool:
    return hash(entity) != hash(candidate) and entity.object_data.lang == candidate.object_data.lang and \
           entity.object_data.object_type == candidate.object_data.object_type


class Detector:
    def detect(self, directory: str, threshold: float, granularity: str) -> DetectionResult:
        raise NotImplemented


class NaiveDetector(Detector):
    def detect(self, directory: str, threshold: float, granularity: str) -> DetectionResult:
        with Profile("EntitiesExtractor.extract_data_from_directory"):
            files, files_data, entities = EntitiesExtractor.extract_data_from_directory(directory, granularity)

        clones = []
        with Profile("Validate candidates set"):
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


@dataclass
class CandidateData:
    is_clone: bool
    score: float


def compute_candidate_similarity(tokens1: List[str], tokens2: List[str], ths: float, gtc: LANGUAGE_ORDER) \
        -> CandidateData:
    max_len = max(len(tokens1), len(tokens2))
    req_matches = ceil(max_len * ths)

    curr_matches = 0
    tok_pos1 = 0
    tok_pos2 = 0
    while tok_pos1 < len(tokens1) and tok_pos2 < len(tokens2):
        if min(len(tokens1) - tok_pos1, len(tokens2) - tok_pos2) + curr_matches >= req_matches:
            if tokens1[tok_pos1] == tokens2[tok_pos2]:
                curr_matches += 1
                tok_pos1 += 1
                tok_pos2 += 1
            else:
                if gtc[tokens1[tok_pos1]] < gtc[tokens2[tok_pos2]]:
                    tok_pos1 += 1
                else:
                    tok_pos2 += 1
        else:
            break

    if curr_matches >= req_matches:
        return CandidateData(True, curr_matches / max_len)
    else:
        return CandidateData(False, curr_matches / max_len)


class FilteringDetector(Detector):
    def __init__(self, max_l_depth: int = 1):
        self.max_l_depth = max_l_depth

    def detect(self, directory: str, threshold: float, granularity: str) -> DetectionResult:
        with Profile("EntitiesExtractor.extract_data_from_directory"):
            files, files_data, entities = EntitiesExtractor.extract_data_from_directory(directory, granularity)
        with Profile("sort_tokens_gtc"):
            gtc = sort_tokens_gtc(entities)
        with Profile("Indexer"):
            indexer = Indexer(entities, self.max_l_depth, threshold)

        clones = []
        considered_pairs = set()
        for i in range(len(entities)):
            entity = entities[i]
            lang = entity.object_data.lang
            tokens = entity.bag_of_tokens

            candidates = set()

            with Profile("Build candidates set"):
                for l_depth in range(1, self.max_l_depth + 1):
                    left_bound, right_bound = get_tokens_bounds(tokens, l_depth, threshold)
                    for token in tokens[left_bound: right_bound]:
                        candidates.update(indexer.get_entities_for_token(token, lang, l_depth))

            with Profile("Validate candidates set"):
                for candidate in candidates:
                    if not _validate_entity_candidate(entity, candidate):
                        continue
                    if (entity, candidate) in considered_pairs or (candidate, entity) in considered_pairs:
                        continue
                    considered_pairs.add((entity, candidate))

                    candidate_data = compute_candidate_similarity(entity.bag_of_tokens, candidate.bag_of_tokens, threshold,
                                                                  gtc[entity.object_data.lang])
                    if candidate_data.is_clone:
                        clones.append(CloneData(entity, candidate, candidate_data.score))

        clones = list(sorted(clones, reverse=True))

        return DetectionResult(clones, f"FilteringDetector({self.max_l_depth}), directory: {directory}, "
                                       f"threshold: {threshold}, granularity: {granularity}")
