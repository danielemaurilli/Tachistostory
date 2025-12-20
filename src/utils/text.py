"""
Text utilities for masking and parsing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List
import re

PUNCTUATION_CHARS = ',.:;?!-_"\''
KEPT_PUNCTUATION = ':.,;,!?'


@dataclass
class TextParseResult:
    words: List[str]
    phrases_list: List[str]
    phrases_total: int
    word_to_phrase_map: List[int]


def mask_word(word: str) -> str:
    """Mask a word by replacing letters and digits with '#'."""
    masked_chars: List[str] = []
    for char in word:
        if char in KEPT_PUNCTUATION or char == " ":
            masked_chars.append(char)
        elif char.isalnum():
            masked_chars.append("#")
        else:
            masked_chars.append("#")
    return "".join(masked_chars)


def split_sentences(full_text: str) -> List[str]:
    """Split text into sentences based on .!? separators."""
    return [s.strip() for s in re.split(r"[.!?]+", full_text) if s.strip()]


def build_words_and_phrase_map(full_text: str) -> TextParseResult:
    """
    Build word list and word-to-phrase mapping aligned with punctuation.
    """
    words: List[str] = []
    mapping: List[int] = []
    phrase_idx = 0
    had_word_in_phrase = False
    trailing_wrappers = '"\'”’)]}»'

    for raw_line in full_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        for raw_token in line.split():
            cleaned = raw_token.strip(PUNCTUATION_CHARS + '1234567890')
            if cleaned:
                words.append(cleaned)
                mapping.append(phrase_idx)
                had_word_in_phrase = True

            token_tail = raw_token.rstrip(trailing_wrappers)
            if re.search(r"[.!?]+$", token_tail) and had_word_in_phrase:
                phrase_idx += 1
                had_word_in_phrase = False

    computed_total = phrase_idx + (1 if had_word_in_phrase else 0)

    phrases_list = split_sentences(full_text)
    phrases_total = len(phrases_list) if phrases_list else computed_total

    if phrases_total > 0:
        mapping = [min(idx, phrases_total - 1) for idx in mapping]

    return TextParseResult(
        words=words,
        phrases_list=phrases_list,
        phrases_total=phrases_total,
        word_to_phrase_map=mapping,
    )
