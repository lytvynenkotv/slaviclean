from typing import List, Tuple


def mask_message(message: str, spans: List[Tuple[int, int]], mask_symbol: str) -> str:
    """Replaces text in the given spans with the mask symbol.

    Args:
        message (str): The original message.
        spans (List[Tuple[int, int]]): A list of tuples representing the start and end indices of text to be masked.
        mask_symbol (str): The symbol used for masking.

    Returns:
        str: The masked message with specified spans replaced by the mask symbol.
    """
    result = []
    last_index = 0

    for start, end in sorted(spans):
        result.append(message[last_index:start])
        result.append(mask_symbol * (end - start))
        last_index = end

    result.append(message[last_index:])

    return ''.join(result)
