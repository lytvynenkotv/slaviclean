from pytest import fixture

from slaviclean import SlaviCleaner


@fixture
def scleaner():
    return SlaviCleaner(preload=True)


def test_sanitize_01(scleaner):
    result = scleaner.sanitize('Сумка сока і супа із кури', lang='uk')
    expect = 'Сумка сока і супа із кури'

    assert result.masked_message == expect
    assert not result.profanities


def test_sanitize_02(scleaner):
    result = scleaner.sanitize('Курва', lang='uk')
    expect = '*****'
    assert result.masked_message == expect


def test_sanitize_03(scleaner):
    result = scleaner.sanitize('К***а', lang='uk')
    expect = '*****'
    assert result.masked_message == expect



def test_sanitize_04(scleaner):
    result = scleaner.sanitize('курррваааааа', lang='uk')
    expect = '************'
    assert result.masked_message == expect


def test_sanitize_05(scleaner):
    result = scleaner.sanitize('курвам', lang='uk')
    expect = '******'
    assert result.masked_message == expect


def test_sanitize_06(scleaner):
    result = scleaner.sanitize('Нафарбована курва', lang='uk')
    expect = '*********** *****'
    assert result.masked_message == expect


def test_sanitize_07(scleaner):
    result = scleaner.sanitize('Н-а-ф-а-р-б-о-в-а-н-а К У Р В А', lang='uk')
    expect = '*********** *****'
    assert result.masked_message == expect


def test_sanitize_08(scleaner):
    result = scleaner.sanitize('кyp8@', lang='uk')
    expect = '*****'
    assert result.masked_message == expect


def test_sanitize_09(scleaner):
    result = scleaner.sanitize('kyrva', lang='surzhyk')
    expect = '*****'

    assert result.masked_message == expect


def test_sanitize_10(scleaner):
    result = scleaner.sanitize('курволика', lang='surzhyk')
    assert result.masked_message == result.message

    result = scleaner.sanitize('курволика', lang='surzhyk', analyze_morph=True)
    expect = '*********'
    assert result.masked_message == expect


def test_sanitize_11(scleaner):
    result = scleaner.sanitize('Ох, курволика!', lang='surzhyk')
    assert result.masked_message == result.message

    result = scleaner.sanitize('Ох, курволика!', lang='surzhyk', analyze_morph=True)
    expect = '**, **********'
    assert result.masked_message == expect

    result = scleaner.sanitize('Ох, курволика!', lang='surzhyk', analyze_morph=True, slevel='minimal')
    assert result.masked_message == result.message


def test_sanitize_12(scleaner):
    result = scleaner.sanitize(
        'От же ж, к у р в а, страхуй, бо об’ївся г***м супом, облив себе соком, ще й сумка, су4k@, відірвалась', lang='surzhyk')
    expect = 'От же ж, *****, страхуй, бо об’ївся ***** супом, облив себе соком, ще й сумка, *****, відірвалась'
    assert result.masked_message == expect
