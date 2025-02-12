from typing import Optional
import re
from dataclasses import dataclass

import pandas as pd

from ..config import LAT_SYMBOLS_MAP_DATA_PATH, CYR_SYMBOLS_MAP_DATA_PATH


__PATTERNS = None


def get_patterns():
    """Retrieves or initializes the global Patterns instance.

    Returns:
        Patterns: The global Patterns instance containing regex patterns for text processing.
    """
    global __PATTERNS
    if not __PATTERNS:
        __PATTERNS = Patterns()
    return __PATTERNS


@dataclass
class Patterns:
    """Stores regex patterns for detecting and handling obfuscated or obscured text."""
    TOKEN_PATTERN: Optional[re.Pattern] = None
    IS_CYRILLIC_TOKEN_PATTERN: Optional[re.Pattern] = None
    HAS_CYRILLIC_IN_TOKEN_PATTERN: Optional[re.Pattern] = None
    IS_LATIN_TOKEN_PATTERN: Optional[re.Pattern] = None

    INNER_LOOK_ALIKE_CYR_CHARS_PATTERN: Optional[re.Pattern] = None

    __CYRILLIC_ALPHABET = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯËЇЙЭЁЫЪ’'
    __LATIN_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ’'

    def __post_init__(self):
        """Initializes regex patterns for text normalization and deobfuscation."""
        self.ABC = self.__CYRILLIC_ALPHABET + self.__LATIN_ALPHABET
        self.PUNCTUATION = ',."()[]{}<>!?\':;-%&#=@^_~|'
        self.TOKEN_PATTERN = re.compile(rf'[^\s{re.escape(self.PUNCTUATION)}](\S*[^\s{re.escape(self.PUNCTUATION)}])?')
        self.IS_CYRILLIC_TOKEN_PATTERN = re.compile(rf"^[{self.__CYRILLIC_ALPHABET}]*$")
        self.IS_LATIN_TOKEN_PATTERN = re.compile(rf"^[{self.__LATIN_ALPHABET}]*$")

        cyr_look_alike_df = pd.read_csv(str(CYR_SYMBOLS_MAP_DATA_PATH))
        lat_look_alike_df = pd.read_csv(str(LAT_SYMBOLS_MAP_DATA_PATH))

        self.CYR_INNER_LOOK_ALIKE_CYR_CHARS = {
            row.lookAlikeChars: row.symbol for _, row in cyr_look_alike_df.iterrows()
        }
        self.CYR_INNER_LOOK_ALIKE_CYR_CHARS_PATTERN = re.compile(
            "|".join(f"({re.escape(row.lookAlikeChars)})" for _, row in cyr_look_alike_df.iterrows())
        )

        self.LAT_INNER_LOOK_ALIKE_CYR_CHARS = {
            row.lookAlikeChars: row.symbol for _, row in lat_look_alike_df.iterrows()
        }
        self.LAT_INNER_LOOK_ALIKE_CYR_CHARS_PATTERN = re.compile(
            "|".join(f"({re.escape(row.lookAlikeChars)})" for _, row in lat_look_alike_df.iterrows())
        )

        self.OBFUSCATION_PATTERNS = {
            sep: re.compile(
                rf'(^|\s)([{self.ABC}]([{re.escape(sep)}][{self.ABC}]){{2,}})([{re.escape(self.PUNCTUATION)}]|\s|$)',
                flags=re.IGNORECASE
            ) for sep in '-.* '
        }

        self.__MASK_SYMBOLS = "#&₴…@*_"
        self.MASKED_OBSCENE_PATTERNS = {
            mask: re.compile(
                rf"(^|\s)([{self.ABC}]+([{re.escape(mask)}]+)[{self.ABC}]+)([{re.escape(self.PUNCTUATION)}]|\s|$)",
                flags=re.IGNORECASE
            ) for mask in self.__MASK_SYMBOLS
        }

        self.PI_START = re.compile(rf'(3[\.,]14)[{self.__CYRILLIC_ALPHABET+self.__LATIN_ALPHABET}]+')
        self.CHAR_REPETITIONS = re.compile(r'(.)\1{2,}')
