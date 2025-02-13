# slaviclean

[![Python Versions](https://img.shields.io/badge/Python%20Versions-%3E%3D3.11-informational)](https://pypi.org/project/nlp-flexi-tools/)
[![Version](https://img.shields.io/badge/Version-0.0.4-informational)](https://pypi.org/project/nlp-flexi-tools/)


**SlaviCleaner** is a profanity filtering library designed for cleaning text from offensive language, specifically tailored for Ukrainian and Russian languages. 
It detects, masks, and reports offensive words while providing different levels of filtering.

This module uses spaCy for natural language processing and employs advanced techniques for detecting profanities,
including handling obfuscated words, variants of swear words, and morphology forms.

### Features

- Detects and masks offensive words in slavic languages (Ukrainian, Russian).
- Handles obfuscated, substituted, and morphologically varied forms of profanity.
- Provides detailed reporting of profanities detected, including the type of relationship (e.g., euphemism, vulgar, loanword).
- Allows the customization of filtering level with three options: `complete`, `basic`, `minimal`.
- Offers support for subtree-level profanity filtering.
- Handles masked and obfuscated profanity patterns effectively.

--- 

## Installation

To install **SlaviCleaner**, run:

```bash
pip install slaviclean
```

--- 

## Usage

### Initializing 

```python
from slaviclean import SlaviCleaner

scleaner = SlaviCleaner()
```
#### Initializing with preloads
You can preload the necessary language models for faster processing. 
The `preload` option loads the models for the supported languages (`uk`, `ru`, `surzhyk`).

```python
from slaviclean import SlaviCleaner

scleaner = SlaviCleaner(preload=True)
```

### Core Functions

#### `get_available_languages()`
Retrieves a set of languages supported by the profanity filter.

- **Returns**:
  - A set of language codes (e.g., `{'uk', 'ru', 'surzhyk'}`).

- **Example**:

```python
from slaviclean import SlaviCleaner

scleaner = SlaviCleaner(preload=True)
languages = scleaner.get_available_languages()

print(languages)  
# Output: {'uk', 'ru', 'surzhyk'}
```


#### `sanitize(message, lang, min_subtree_size, mask_symbol, slevel, analyze_morph)`
Filters profanities from the given message and returns a detailed report.

- **Arguments**:
  - `message` (str): The input message to filter.
  - `lang` (str): The language of the message (supports `'uk'`, `'ru'`, and `'surzhyk'`, default is `'surzhyk'`).
  - `min_subtree_size` (float): Minimum size of the token subtree for dependency parsing (default is `3`).
  - `mask_symbol` (str): Symbol used to mask profanities (default is `'*'`).
  - `slevel` (str): Severity level of filtering (can be `'complete'`, `'basic'`, or `'minimal'`, default is `'complete'`).
  - `analyze_morph` (bool): Whether to analyze the morphology of words (default is `False`).

- **Returns**:
  - A `SanitizeReport` containing the masked message and list of detected profanities.

- **Example**:

```python
from slaviclean import SlaviCleaner

scleaner = SlaviCleaner(preload=True)
message = "От же ж, к у р в а, страхуй, бо об’ївся г***м супом, облив себе соком, ще й сумка, су4k@, відірвалась"
 
sanitize_report = scleaner.sanitize(message, lang='uk')

print(sanitize_report)  
# Output: 
#   SanitizeReport(
#      message='От же ж, курва, страхуй, бо об’ївся г***м супом, облив себе соком, ще й сумка, су4k@, відірвалась', 
#      masked_message='От же ж, *****, страхуй, бо об’ївся ***** супом, облив себе соком, ще й сумка, *****, відірвалась', 
#      profanities=[
#           Profanity(span=(9, 14), nearest='курва', tags=['vulgar', 'euphemism', 'loanword']), 
#           Profanity(span=(36, 41), nearest='г***м', tags=['masked']), 
#           Profanity(span=(79, 84), nearest='сучка', tags=['insulting', 'slur', 'vulgar'])])

```

### Available Severity Levels

- **`complete`**  
  Cleans all profanities, including euphemisms, vulgarities, and loanwords.  
- **`basic`**  
  Cleans more aggressive profanity, without including euphemisms.  
- **`minimal`**  
  Only cleans the most offensive words.


### Supported Languages

**SlaviCleaner** currently supports the following languages:
- **Ukrainian (`uk`)**
- **Russian (`ru`)**
- **Surzhyk (`surzhyk`)**

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- The **spaCy** library is used for NLP tasks like tokenization, part-of-speech tagging, and dependency parsing.
- The **pymorphy3** library is used for morphological analysis.
