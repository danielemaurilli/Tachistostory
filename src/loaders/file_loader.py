"""
File loading utilities for text and Word documents.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List
from src.core.config import MusicConfig
import os

import docx2txt

from src.utils.text import TextParseResult, build_words_and_phrase_map


@dataclass
class LoadedText:
    words: List[str]
    phrases_list: List[str]
    phrases_total: int
    word_to_phrase_map: List[int]

class FileLoader:
    """Load and parse text files into word/phrase structures."""

    @staticmethod
    def load_txt(path: str) -> LoadedText:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, "r", encoding="utf-8") as file:
            text = file.read()

        parse_result = build_words_and_phrase_map(text)
        if not parse_result.words:
            raise ValueError("Il file è vuoto")

        return FileLoader._to_loaded_text(parse_result)

    @staticmethod
    def load_docx(path: str) -> LoadedText:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        text = docx2txt.process(path)
        parse_result = build_words_and_phrase_map(text)
        if not parse_result.words:
            raise ValueError("Word document appears to be empty after conversion.")

        return FileLoader._to_loaded_text(parse_result)

    @staticmethod
    def _to_loaded_text(parse_result: TextParseResult) -> LoadedText:
        return LoadedText(
            words=parse_result.words,
            phrases_list=parse_result.phrases_list,
            phrases_total=parse_result.phrases_total,
            word_to_phrase_map=parse_result.word_to_phrase_map,
        )

class LoadMusic:
    @staticmethod
    def load_background_music(path: str) -> MusicConfig:
        if not os.path.exists(path):
            raise FileNotFoundError(f'File not found: {path}')
        return MusicConfig(background_music=path)