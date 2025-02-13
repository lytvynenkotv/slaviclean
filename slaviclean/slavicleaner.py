from typing import List, Dict, Set, Tuple, Optional
import logging
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

import spacy
from spacy.util import is_package
import spacy.tokens

from flexi_nlp_tools.flexi_dict import FlexiDict

from .profanity_dict_builder import build_profanity_dict
from .preprocessor import get_patterns, deobfuscate_token, deobfuscate_message, mask_message, MorphAnalyzer
from .sanitize_report import SanitizeReport
from .profanity import Profanity, ProfanityRelationType, TAG_LEVEL_MAP
from .config import (
    SPACY_MODEL_UK,
    SPACY_MODEL_RU,
    MIN_SUBTREE_SIZE
)


logger = logging.getLogger(__name__)


_SPACY_MODELS = {
    'uk': SPACY_MODEL_UK,
    'ru': SPACY_MODEL_RU,
}


class SLevel(Enum):

    COMPLETE = 'complete'
    BASIC = 'basic'
    MINIMAL = 'minimal'


class SlaviCleaner:
    """Profanity filtering class that detects and masks offensive words."""

    _nlp: Dict[str, spacy.Language] = None
    _vocab: Dict[str, FlexiDict] = None
    _morph: MorphAnalyzer = None

    def __init__(self, preload: bool = False, keyboards: List[str] = None):
        self._morph = MorphAnalyzer()
        self._vocab = {}
        self._nlp = {}

        if preload:
            self.preload_models(keyboards=keyboards)

    def sanitize(
            self,
            message: str,
            lang: str = 'surzhyk',
            min_subtree_size: float = MIN_SUBTREE_SIZE,
            mask_symbol: str = '*',
            slevel: str = "complete",
            analyze_morph: bool = False
    ) -> SanitizeReport:
        """Filters profanities from the given message.

        Args:
            message (str): The input message to filter.
            lang (str): Language code (default: 'uk').
            min_subtree_size (float): Minimum subtree size for dependency parsing.
            mask_symbol (str): Symbol used to mask profanities.

        Returns:
            ProfanityFilterOutput: Contains the masked message and list of profanities.
        """
        available_languages = self.get_available_languages()
        if lang not in available_languages:
            raise ValueError(f"Unsupported language: {lang}. Only {available_languages} are supported.")

        message = deobfuscate_message(message)
        profanities = self._get_profanities(message, lang, min_subtree_size, analyze_morph)

        match SLevel(slevel):
            case SLevel.COMPLETE: level = 3
            case SLevel.BASIC: level = 2
            case SLevel.MINIMAL: level = 1
            case _: level = 3

        spans = [p.span for p in profanities if min(TAG_LEVEL_MAP[tag] for tag in p.tags) <= level]

        masked_message = mask_message(message, spans, mask_symbol)

        return SanitizeReport(message, masked_message, profanities)

    def _get_profanities(self, message: str, lang: str, min_subtree_size: float, analyze_morph: bool) -> List[Profanity]:
        """Detects profanities and masked profanities in the given message."""

        self._check_language(lang)

        doc = self._parse(message, lang)

        def __process_token(token):
            return token.i, self._check_token(token, lang, analyze_morph)

        with ThreadPoolExecutor() as executor:
            results = executor.map(__process_token, doc)

        token_idx2profanity = dict(results)

        for token in doc:
            _profanity = self._check_token(token, lang, analyze_morph)
            token_idx2profanity[token.i] = _profanity

        for token in doc:
            if token_idx2profanity.get(token.i):

                for i_token in self._get_token_subtree(token, min_subtree_size=min_subtree_size):
                    if token_idx2profanity.get(i_token):
                        continue
                    token_idx2profanity[i_token] = Profanity(
                        span=(doc[i_token].idx, doc[i_token].idx + len(doc[i_token].orth_)),
                        nearest=token_idx2profanity[token.i].nearest,
                        tags=token_idx2profanity[token.i].tags + [ProfanityRelationType.SUBTREE.value, ])

        return [x for x in token_idx2profanity.values() if x is not None]

    def _check_token(self, token, lang, analyze_morph):
        if token.pos_ in ('PUNCT', 'CCONJ', 'SCONJ', 'PART', 'DET', 'ADP'):
            return None

        if self._is_masked_profanity(token.orth_):
            logger.debug(f'\t- detected masked')
            return Profanity(
                span=(token.idx, token.idx + len(token.orth_)),
                nearest=token.orth_,
                tags=[ProfanityRelationType.MASKED.value, ])


        candidates = deobfuscate_token(token.orth_, lang)
        for candidate in candidates:
            profanity = self._is_known_profanity(candidate, span=(token.idx, token.idx + len(token.orth_)), lang=lang)
            if profanity is None:
                continue
            return profanity

        if analyze_morph:

            morph_forms = set().union(*[self._morph.collect_morph_forms(candidate, lang) for candidate in candidates])

            for candidate in morph_forms:
                profanity = self._is_known_profanity(candidate, span=(token.idx, token.idx + len(token.orth_)), lang=lang)
                if profanity is None:
                    continue
                return profanity

    @staticmethod
    def _get_token_subtree(token: spacy.tokens.Token, min_subtree_size: float) -> List[int]:
        """Extracts token indices from a subtree if it meets size criteria."""
        for t in token.doc:
            logger.debug(t.orth_, t.dep_, t.head)
        subtree = [sub.i for sub in token.subtree if sub.pos_ != "PUNCT"]
        subtree_size = sum(len(sub.orth_) for sub in token.subtree)
        if subtree_size and len(token.orth_) / subtree_size >= min_subtree_size:
            return subtree

        return []

    @staticmethod
    def _is_masked_profanity(token: str):
        """Checks if the token matches a masked profanity pattern"""
        patterns = get_patterns()
        return patterns.MASKED_OBSCENE_PATTERNS['*'].match(token) is not None

    def _is_known_profanity(self, token: str, span: Tuple[int, int], lang: str):
        profanity_candidates = self._search_internal(token.lower(), lang)
        if not profanity_candidates:
            return None
        
        profanity_candidate = profanity_candidates[0]
        similarity = .75 - profanity_candidate.total_corrections_price
        if similarity <= 0:
            return None
        
        profanity_candidate_types = sorted(
            profanity_candidate.value.split(' '),
            key=lambda x: TAG_LEVEL_MAP[x]
        )
        return Profanity(
            span=span,
            nearest=profanity_candidate.path,
            tags=profanity_candidate_types)
    
    def _load_parser(self, lang: str):

        if lang == 'surzhyk':
            lang = 'uk'

        if not self._nlp:
            self._nlp = {}

        if not self._nlp.get(lang):
            self._check_language(lang)

            if not is_package(_SPACY_MODELS[lang]):
                logger.info(f'Downloading spaCy model for language: {lang}')

                from spacy.cli import download
                download(_SPACY_MODELS[lang])
                logger.info(f'Model for language {lang} downloaded successfully.')

            logger.info(f'Loading spaCy model for language: {lang}')
            self._nlp[lang] = spacy.load(_SPACY_MODELS[lang])
            logger.info(f'Model for language {lang} loaded successfully.')

        return self._nlp[lang]

    @staticmethod
    def get_available_languages() -> Set[str]:
        return {'uk', 'ru', 'surzhyk'}

    def _check_language(self, lang: str):
        available_languages = self.get_available_languages()
        if lang not in available_languages:
            raise ValueError(f"Unsupported language: {lang}. Only {available_languages} are supported.")

    def preload_models(self, lang: Optional[str] = None, keyboards: Optional[List[str]] = None):
        if lang:
            self._vocab[lang] = build_profanity_dict(lang=lang, keyboards=keyboards)
            self._load_parser(lang)
            self._morph.preload_model(lang)
            return

        for lang in self.get_available_languages():
            self._vocab[lang] = build_profanity_dict(lang=lang, keyboards=keyboards)
            self._load_parser(lang)
            self._morph.preload_model(lang)

    def _parse(self, message: str, lang: str):
        if lang == 'surzhyk':
            lang = 'uk'
        if not self._nlp or not self._nlp.get(lang):
            self._load_parser(lang)
        return self._nlp[lang](message)

    def _search_internal(self, token: str, lang: str):

        if not self._vocab:
            self._vocab = {}

        if lang not in self._vocab:
            self._vocab[lang] = build_profanity_dict(lang)

        return self._vocab[lang].search_internal(token)

