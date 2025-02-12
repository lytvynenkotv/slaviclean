from typing import Set

from flexi_nlp_tools.lite_translit import en2uk_translit

from .patterns_loader import get_patterns


def deobfuscate_message(message: str) -> str:
    """Removes obfuscation from a given message by replacing special characters and patterns.

    Args:
        message (str): The input message potentially containing obfuscated obscene words.

    Returns:
        str: The cleaned message with obfuscation removed.
    """
    patterns = get_patterns()

    for sep, pattern in patterns.OBFUSCATION_PATTERNS.items():
        upd_message = message
        for match in pattern.finditer(message):
            sub_from = match.group(2)
            sub_to = sub_from.replace(sep, '')
            upd_message = upd_message.replace(sub_from, sub_to)
        message = upd_message

    for mask, pattern in patterns.MASKED_OBSCENE_PATTERNS.items():
        upd_message = message
        for match in pattern.finditer(message):
            sub_from = match.group(2)
            sub_to = sub_from.replace(mask, '*')
            upd_message = upd_message.replace(sub_from, sub_to)
        message = upd_message

    return message


def deobfuscate_token(token: str, lang: str) -> Set[str]:
    """Generates possible deobfuscated versions of a token.

    Args:
        token (str): The input token to be deobfuscated.
        lang (str): The language of the token (e.g., 'ru', 'uk', 'surzhyk').

    Returns:
        Set[str]: A set of possible deobfuscated versions of the token.
    """
    if lang == 'surzhyk':
        lang = 'uk'

    def __replace_cyr_inner_look_alike_match(match):
        for group_index, group in enumerate(match.groups(), start=1):
            if group:
                return patterns.CYR_INNER_LOOK_ALIKE_CYR_CHARS[match.group(group_index)]
        return match.group(0)

    def __replace_lat_inner_look_alike_match(match):
        for group_index, group in enumerate(match.groups(), start=1):
            if group:
                return patterns.LAT_INNER_LOOK_ALIKE_CYR_CHARS[match.group(group_index)]
        return match.group(0)

    patterns = get_patterns()

    deobfuscated = {token.lower(), }

    deobfuscated.add(patterns.CHAR_REPETITIONS.sub(r'\1\1', token).lower())
    deobfuscated.add(patterns.CHAR_REPETITIONS.sub(r'\1', token).lower())

    if lang in ('ru', 'uk'):
        start_with_pi = patterns.PI_START.match(token.upper())
        if start_with_pi:
            token = token.replace(start_with_pi.group(1), 'пи' if lang == 'ru' else 'пі')
            deobfuscated.add(token)

        if patterns.IS_CYRILLIC_TOKEN_PATTERN.match(token.upper()):
            return deobfuscated

        token_fixed_look_alike = patterns.CYR_INNER_LOOK_ALIKE_CYR_CHARS_PATTERN.sub(__replace_cyr_inner_look_alike_match, token)

        if patterns.IS_CYRILLIC_TOKEN_PATTERN.match(token_fixed_look_alike.upper()):
            deobfuscated.add(token_fixed_look_alike.lower())

        token_translit = en2uk_translit(token)
        deobfuscated.add(token_translit.lower())

        token_translit = en2uk_translit(token_fixed_look_alike)
        deobfuscated.add(token_translit.lower())
    else:
        token_fixed_look_alike = patterns.LAT_INNER_LOOK_ALIKE_CYR_CHARS_PATTERN.sub(__replace_lat_inner_look_alike_match, token)
        deobfuscated.add(token_fixed_look_alike.lower())

    return deobfuscated
