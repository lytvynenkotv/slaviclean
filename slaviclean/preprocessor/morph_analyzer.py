"""MorphAnalyzer class used for collecting token morph forms."""
import logging
import re
from typing import List, Optional, Set

import pymorphy3


class MorphAnalyzer:
    """Functionality for collecting token morph forms."""

    def __init__(self, preload: bool = False):
        """Init MorphAnalyzer."""
        self._morph = {}

        if preload:
            self.preload_model('uk')
            self.preload_model('ru')

    def preload_model(self, lang: str):
        if lang == 'surzhyk':
            lang = 'uk'
        self._morph[lang] = pymorphy3.MorphAnalyzer(lang=lang)

    def _parse(self, token: str, lang: str):
        if lang == 'surzhyk':
            lang = 'uk'
        if lang not in self._morph:
            self.preload_model(lang)
        return self._morph[lang].parse(token) or []

    def collect_morph_forms(self, token: str, lang: str) -> Set[str]:
        parsed = self._parse(token, lang)

        morph_forms: Set[str] = set()

        for p in parsed:
            for method in p.methods_stack:

                method_name = method[0].__str__()[: method[0].__str__().find("(")]
                s = method[1]
                if len(s) < 2:
                    continue

                if method_name == "DictionaryAnalyzer" or method_name.startswith("Unknown"):
                    morph_forms.add(s)

        return morph_forms
