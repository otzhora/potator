import os
from collections import defaultdict, Counter
from difflib import HtmlDiff
from typing import List, Dict

from potator.models import DetectionResult, EntityData


HTML_HEADER = """
<head>
<meta http-equiv="Content-Type"
      content="text/html; charset=ISO-8859-1" />
<title></title>
<style type="text/css">
    table.diff {font-family:Courier; border:medium;}
    .diff_header {background-color:#e0e0e0}
    td.diff_header {text-align:right}
    .diff_next {background-color:#c0c0c0}
    .diff_add {background-color:#aaffaa}
    .diff_chg {background-color:#ffff77}
    .diff_sub {background-color:#ffaaaa}
</style>
</head>
"""


def get_formatted_detection_result(result: DetectionResult) -> str:
    differ = HtmlDiff()

    algorithm = f"Algorithm '{result.used_algorithm}' was used to get those results <br>"
    clones = result.clones
    tables = []
    for clone in clones:
        code1 = clone.entity_1.object_data.content.splitlines()
        code2 = clone.entity_2.object_data.content.splitlines()
        src1 = clone.entity_1.file_path
        src2 = clone.entity_2.file_path
        score = clone.similarity
        table = differ.make_table(code1, code2, fromdesc=f"{src1}, similarity: {score}", todesc=src2, context=True)
        tables.append(table)
        tables.append("<br>")
    return f"<html><body> {HTML_HEADER} {algorithm} {''.join(tables)} </body></html>"


def write_formatted_detection_result(result: DetectionResult, out: str) -> None:
    html = get_formatted_detection_result(result)
    with open(out, "w") as f:
        f.write(html)


def make_absolute_path(path: str) -> str:
    if os.path.isabs(path):
        return path
    return os.path.join(os.getcwd(), path)


LANGUAGE_ORDER = Dict[str, int]


def build_global_token_counts_from_entities(entities: List[EntityData]) -> Dict[str, LANGUAGE_ORDER]:
    global_token_counts = defaultdict(Counter)
    for entity in entities:
        global_token_counts[entity.object_data.lang] += Counter(entity.bag_of_tokens)

    return global_token_counts


def sort_tokens_gtc(entities: List[EntityData]) -> Dict[str, LANGUAGE_ORDER]:
    global_token_counts = build_global_token_counts_from_entities(entities)

    for entity in entities:
        lang_token_counts = global_token_counts[entity.object_data.lang]
        entity.bag_of_tokens.sort(key=lambda token: lang_token_counts[token])
    return global_token_counts
