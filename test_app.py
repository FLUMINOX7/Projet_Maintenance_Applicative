from app_functions import convert


def test_convert_eur_usd():
    rates = {"EUR": 1.0, "USD": 1.1}
    assert round(convert(10.0, "EUR", "USD", rates), 2) == 11.0


def test_convert_same_currency_returns_none():
    rates = {"EUR": 1.0, "USD": 1.1}
    assert convert(10.0, "EUR", "EUR", rates) is None


def test_convert_zero_returns_none():
    rates = {"EUR": 1.0, "USD": 1.1}
    assert convert(0.0, "EUR", "USD", rates) is None


def test_convert_negative_returns_none():
    rates = {"EUR": 1.0, "USD": 1.1}
    assert convert(-5.0, "EUR", "USD", rates) is None
