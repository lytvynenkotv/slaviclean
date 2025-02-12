from enum import Enum
from typing import Tuple, List
from dataclasses import dataclass


class ProfanityRelationType(Enum):

    """Defines types of profanity relations."""

    INSULTING = "insulting"
    # INSULTING: Offensive or rude words aimed at humiliating, degrading, or verbally attacking someone.
    # These words can be directed at a person's intelligence, appearance, behavior, or other personal traits.
    # Example: "Idiot," "moron," "loser."

    OBSCENE = "obscene"
    # OBSCENE: Profane, explicit, or offensive language, usually referring to sexual, bodily, or taboo subjects.
    # Often used in strong emotional expressions.
    # Example: "Fuck," "shit," "cunt."

    VULGAR = "vulgar"
    # VULGAR: Crude, colloquial, and sometimes offensive words used in everyday informal speech.
    # These words may not be as strong as obscene language but are considered inappropriate in formal settings.
    # Example: "Damn," "crap," "piss."

    EUPHEMISM = "euphemism"
    # EUPHEMISM: A milder or indirect word or phrase used instead of a harsher or offensive one,
    # often to soften the impact of profanity.
    # Example: "Freaking" (instead of "fucking"), "dang" (instead of "damn").

    SLUR = 'slur'
    # SLUR: A derogatory term used to insult or demean someone based on their personal attributes,
    # often related to sexual orientation, gender, or identity.
    # Example: Certain homophobic or transphobic terms.

    ETHNIC_SLUR = 'ethnic_slur'
    # ETHNIC_SLUR: A pejorative term used to insult or demean someone based on their ethnicity, race, or nationality.
    # Example: Certain racial or national stereotypes.

    LOANWORD = 'loanword'
    # LOANWORD: A profanity or offensive word borrowed from another language,
    # often retaining its original offensive meaning or acquiring a similar function in the borrowing language.
    # Example: "Kurwa" (from Polish), "fuck" (from English), "scheiße" (from German).

    MASKED = "masked"
    # MASKED: A profanity that is partially or fully obscured using symbols (e.g., '*', '#', '!', etc.), making it less explicit but still recognizable.
    # Example: "f**k", "sh#t", "b!tch".

    SUBTREE = "subtree"
    # SUBTREE: A word that is syntactically dependent on a profanity in a sentence, often modifying or being modified by it.
    # Example: In "fucking idiot", "idiot" is in a dependency relationship with "fucking".


TAG_LEVEL_MAP = {
    ProfanityRelationType.OBSCENE.value: 1,
    ProfanityRelationType.MASKED.value: 1,
    ProfanityRelationType.INSULTING.value: 2,
    ProfanityRelationType.SLUR.value: 2,
    ProfanityRelationType.ETHNIC_SLUR.value: 2,
    ProfanityRelationType.VULGAR.value: 3,
    ProfanityRelationType.EUPHEMISM.value: 3,
    ProfanityRelationType.LOANWORD.value: 3,
    ProfanityRelationType.SUBTREE.value: 4,
}


@dataclass
class Profanity:
    """Represents a detected profanity in the message."""
    span: Tuple[int, int]
    # span: start and end index of the profanity in the message

    nearest: str
    # nearest: original or nearest profanity match

    tags: List[ProfanityRelationType]
    # types: A set of profanity relation types, indicating the nature of the detected profanity
    # (e.g., direct profanity, obscene, masked profanity, dependency relation, etc.).
