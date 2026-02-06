"""
Word Manager - Gestione parole, frasi e file di testo.
"""
from typing import List, Optional

from src.loaders.file_loader import FileLoader, LoadedText
from src.utils.text import mask_word


class WordManager:
    """Gestisce il caricamento e la navigazione di parole/frasi."""

    def __init__(self):
        # File state
        self.file_loaded = False
        self.file_name: Optional[str] = None
        
        # Word data
        self.words: List[str] = []
        self.word_count: int = 0
        self.current_index: int = 0
        self.current_word: str = ""
        self.masked_word: str = ""
        
        # Phrase data
        self.phrases: List[str] = []
        self.phrase_index: int = 0
        self.phrase_count: int = 0
        self.word_to_phrase_map: List[int] = []

    @property
    def has_words(self) -> bool:
        return len(self.words) > 0

    @property
    def is_at_start(self) -> bool:
        return self.current_index == 0

    @property
    def is_at_end(self) -> bool:
        return self.current_index >= len(self.words) - 1

    def load_txt(self, file_path: str) -> List[str]:
        """Carica parole da un file di testo."""
        loaded = FileLoader.load_txt(file_path)
        self._apply_loaded_text(loaded)
        return self.words

    def load_docx(self, file_path: str) -> List[str]:
        """Carica parole da un documento Word."""
        loaded = FileLoader.load_docx(file_path)
        self._apply_loaded_text(loaded)
        return self.words

    def _apply_loaded_text(self, loaded: LoadedText) -> None:
        """Applica i dati caricati allo stato."""
        self.words = loaded.words
        self.word_to_phrase_map = loaded.word_to_phrase_map
        self.phrases = loaded.phrases_list
        self.phrase_count = loaded.phrases_total
        self.word_count = len(self.words)

        if self.words:
            self.set_index(0)
        else:
            self._clear_current()

    def set_index(self, index: int) -> None:
        """Imposta l'indice corrente (con clamp)."""
        if not self.words:
            return

        index = max(0, min(index, len(self.words) - 1))
        self.current_index = index
        self.current_word = self.words[index]
        self.masked_word = mask_word(self.current_word)
        self._sync_phrase_index()

    def go_next(self) -> bool:
        """Avanza alla parola successiva. Ritorna True se avanzato."""
        if self.is_at_end:
            return False
        self.set_index(self.current_index + 1)
        return True

    def go_previous(self) -> bool:
        """Torna alla parola precedente. Ritorna True se tornato."""
        if self.is_at_start:
            return False
        self.set_index(self.current_index - 1)
        return True

    def _sync_phrase_index(self) -> None:
        """Sincronizza l'indice della frase con la parola corrente."""
        if self.word_to_phrase_map and 0 <= self.current_index < len(self.word_to_phrase_map):
            self.phrase_index = self.word_to_phrase_map[self.current_index]
        else:
            self.phrase_index = 0

    def _clear_current(self) -> None:
        """Pulisce lo stato corrente."""
        self.current_index = 0
        self.current_word = ""
        self.masked_word = ""
        self.phrase_index = 0

    def reset(self) -> None:
        """Resetta completamente lo stato."""
        self.file_loaded = False
        self.file_name = None
        self.words = []
        self.word_count = 0
        self.phrases = []
        self.phrase_index = 0
        self.phrase_count = 0
        self.word_to_phrase_map = []
        self._clear_current()
