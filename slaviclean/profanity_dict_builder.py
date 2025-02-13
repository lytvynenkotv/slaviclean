import pandas as pd

from .config import PROFANITY_FILTER_DATA_PATH


def build_profanity_dict(lang: str):
    df = _read_dataset(lang)
    return {
        row.flexion.strip().lower(): row.profanityTypes
        for i, row in df.drop_duplicates(subset=['flexion', ]).iterrows()
    }


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
