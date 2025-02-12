import importlib.resources as pkg_resources
import os
from pathlib import Path

import pkg_resources

DATA_PATH = Path(pkg_resources.resource_filename('slaviclean', 'resources'))
PROFANITY_FILTER_DATA_PATH = DATA_PATH / 'profanity'
CYR_SYMBOLS_MAP_DATA_PATH = DATA_PATH / 'cyrillic_look_alike_map.csv'
LAT_SYMBOLS_MAP_DATA_PATH = DATA_PATH / 'latin_look_alike_map.csv'

# Minimum length ratio of an obscene to a subtree to mask the entire subtree
MIN_SUBTREE_SIZE: float = float(os.getenv('MIN_SUBTREE_SIZE', 0.3))

# Language spaCy models
SPACY_MODEL_UK: str = os.getenv("SPACY_MODEL_UK", "uk_core_news_md")
SPACY_MODEL_RU: str = os.getenv("SPACY_MODEL_RU", 'ru_core_news_md')
