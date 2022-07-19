from .digital import chinese_to_number as chinese_to_number, is_chinese_number as is_chinese_number
from .loader import ResourceLoader as ResourceLoader
from .tools import StringHelper as StringHelper
from .word import Word as Word
from _typeshed import Incomplete

class BaseSegmentProcess:
    group_marker: Incomplete
    string_helper: Incomplete
    segment_type: str
    def __init__(self, **kwargs) -> None: ...
    def split_by_text_groups(self, word, text_groups): ...
    def process(self, word): ...

class SimpleSegmentProcess(BaseSegmentProcess):
    loader: Incomplete
    seg_model: Incomplete
    segment_type: str
    def __init__(self, **kwargs) -> None: ...
    def process(self, word): ...
    def label_sequence(self, words, nbest: int = ...): ...
    def segment(self, label, pre_label_words): ...

class KeywordsSegmentProcess(SimpleSegmentProcess):
    def __init__(self, **kwargs) -> None: ...
    def process(self, word): ...
    def crf_keywords(self, word, nbest: int = ...): ...
    def segment(self, labels, pre_label_words): ...
    @classmethod
    def combine_by_words_list(cls, pre_label_words, words_list): ...

class PinyinSegmentProcess(BaseSegmentProcess):
    loader: Incomplete
    trie: Incomplete
    segment_type: str
    def __init__(self, **kwargs) -> None: ...
    def process(self, words): ...
    def segment(self, text): ...

class BreakSegmentProcess(BaseSegmentProcess):
    loader: Incomplete
    tree: Incomplete
    break_regex_method: Incomplete
    segment_type: str
    def __init__(self, **kwargs) -> None: ...
    def process(self, words): ...

class CombineSegmentProcess(BaseSegmentProcess):
    loader: Incomplete
    trie: Incomplete
    combine_regex_method: Incomplete
    def __init__(self, **kwargs) -> None: ...
    def process(self, words): ...

class TaggingProcess:
    string_helper: Incomplete
    loader: Incomplete
    tagging_model: Incomplete
    def __init__(self, **kwargs) -> None: ...
    def label_tagging(self, words): ...
    def process(self, words): ...
    @classmethod
    def tagging(cls, label): ...

class TagExtractProcess:
    string_helper: Incomplete
    loader: Incomplete
    idf_table: Incomplete
    default_idf: Incomplete
    ntop: Incomplete
    def __init__(self, **kwargs) -> None: ...
    def process(self, words): ...

processes: Incomplete