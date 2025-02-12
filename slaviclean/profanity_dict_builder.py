from typing import List
from itertools import chain

import pandas as pd

from flexi_nlp_tools.flexi_dict import FlexiDict
from flexi_nlp_tools.flexi_dict.search_engine import SearchEngine
from flexi_nlp_tools.flexi_dict.utils import calculate_symbols_distances, calculate_symbols_weights

from .config import PROFANITY_FILTER_DATA_PATH


def build_profanity_dict(lang: str, keyboards: List[str] = None):
    """Builds a profanity dictionary for a given language.

    Args:
        lang (str): The target language ('uk', 'ru', or 'surzhyk').
        keyboards (List[str], optional): Keyboard layouts to consider for symbol distance calculations. Defaults to None.

    Returns:
        FlexiDict: A dictionary with profane words and their types.
    """
    df = _read_dataset(lang)

    # Calculating symbol weights
    corpus = [flexion.strip().lower() for flexion in df['flexion'].values]
    symbols_weights = calculate_symbols_weights(corpus)

    # Calculating symbol distances
    symbols_distances = calculate_symbols_distances(symbol_keyboards=keyboards) if keyboards else None

    search_engine = SearchEngine(symbols_distances=symbols_distances, symbol_weights=symbols_weights)
    profanity_dict = FlexiDict(search_engine=search_engine)

    for (flexion, lemma), sub in df.groupby(by=['flexion', 'lemma']):
        flexion = flexion.strip().lower()

        if not flexion:
            continue

        profanity_types = ' '.join([
            x.strip()
            for x in set(chain(*[
                row.split(' ') for row in sub.profanityTypes.values
            ])) if x.strip()])

        profanity_dict[flexion] = profanity_types

    return profanity_dict


def _read_dataset(lang: str):
    """Reads the profanity dataset for the specified language.

    Args:
        lang (str): The target language ('uk', 'ru', or 'surzhyk').

    Returns:
        pd.DataFrame: The profanity dataset.

    Raises:
        ValueError: If the specified language is not supported.
    """
    if lang == 'surzhyk':
        df = pd.concat((
            pd.read_csv(PROFANITY_FILTER_DATA_PATH / 'uk.csv'),
            pd.read_csv(PROFANITY_FILTER_DATA_PATH / 'ru.csv')))
    elif lang == 'uk':
        df = pd.read_csv(PROFANITY_FILTER_DATA_PATH / 'uk.csv')
    elif lang == 'ru':
        df = pd.read_csv(PROFANITY_FILTER_DATA_PATH / 'ru.csv')
    else:
        raise ValueError(f'Unsupported language; expected one of uk, ru, surzhyk, got {lang}')

    return df
