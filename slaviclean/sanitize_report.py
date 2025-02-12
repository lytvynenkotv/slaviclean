from dataclasses import dataclass
from typing import List

from .profanity import Profanity


@dataclass
class SanitizeReport:
    """Holds the output of the profanity filter.

    Attributes:
        message (str): Original input message.
        masked_message (str): Message with profanities masked.
        profanities (List[Profanity]): List of detected profanities.
    """
    message: str  # Original input message
    masked_message: str  # Message with profanities masked
    profanities: List[Profanity]  # List of detected profanities
