from .tokenizer.identifiers_extractor.parsing import get_tokens


def get_tokens_as_list(file: str, lang: str):
    return get_tokens(file, lang)
