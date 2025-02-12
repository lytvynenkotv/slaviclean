from slaviclean.preprocessor import deobfuscate_message, deobfuscate_token


def test_deobfuscate_token_01():
    token = '4yд0вий'
    expect = 'чудовий'
    assert expect in deobfuscate_token(token, 'uk')


def test_deobfuscate_token_02():
    token = 'пo8iд0мле|-|Hя'
    expect = 'повідомлення'
    assert expect in deobfuscate_token(token, 'uk')


def test_deobfuscate_token_03():
    token = 'Test'
    assert deobfuscate_token(token, 'uk') == {'test', 'тест'}


def test_deobfuscate_token_04():
    token = 'neshchastia'
    expect = 'нещастя'
    assert expect in deobfuscate_token(token, 'uk')


def test_deobfuscate_token_05():
    token = 'BA}|{|<0'
    expect = 'важко'
    assert expect in deobfuscate_token(token, 'uk')


def test_deobfuscate_token_06():
    token = '3,14тест'
    expect = 'пітест'
    assert expect in deobfuscate_token(token, 'uk')


def test_deobfuscate_token_07():
    token = 'sychka'
    expect = 'сучка'
    assert expect in deobfuscate_token(token, 'uk')


def test_deobfuscate_token_08():
    token = 'тееессссссттт'
    expect = 'тест'
    assert expect in deobfuscate_token(token, 'uk')


def test_deobfuscate_message_01():
    message = "П Р И К Л А Д Т-е-к-с-т-у із обф____ією"
    expect = "приклад тексту із обф****ією"
    assert deobfuscate_message(message).lower() == expect.lower()


def test_deobfuscate_message_02():
    message = "П Р И К Л А Д, Т-е-к-с-т-у! із обф____ією;"
    expect = "приклад, тексту! із обф****ією;"
    assert deobfuscate_message(message).lower() == expect.lower()
