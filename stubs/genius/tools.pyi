from _typeshed import Incomplete

class StringHelper:
    digit_range: str
    alpha_range: str
    whitespace_range: str
    halfwidth_punctuation_range: str
    fullwidth_punctuation_range: str
    punctuation_range: Incomplete
    digit_pattern: Incomplete
    alpha_pattern: Incomplete
    whitespace_pattern: Incomplete
    halfwidth_punctuation_pattern: Incomplete
    punctuation_pattern: Incomplete
    cjk_pattern: Incomplete
    @classmethod
    def mark_text(cls, text): ...
    @classmethod
    def halfwidth_to_fullwidth(cls, word): ...
    @classmethod
    def fullwidth_to_halfwidth(cls, word): ...
