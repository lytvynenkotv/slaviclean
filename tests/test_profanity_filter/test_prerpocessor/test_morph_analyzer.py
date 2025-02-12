from pytest import fixture

from slaviclean.preprocessor.morph_analyzer import MorphAnalyzer

@fixture
def morph_analyzer():
    return MorphAnalyzer()


def test_collect_morph_forms_01(morph_analyzer):
    morph_forms = morph_analyzer.collect_morph_forms('темнокоричневый', 'ru')
    assert 'коричневый' in morph_forms
    assert 'темно' in morph_forms
