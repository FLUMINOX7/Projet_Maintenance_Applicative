from app_functions import FALLBACK_RATES, convert, fetch_rates, validate_conversion


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


def test_fetch_rates_uses_local_fallback_without_api_key(monkeypatch):
    monkeypatch.delenv("EXCHANGERATE_API_KEY", raising=False)

    rates = fetch_rates("EUR")

    assert rates == FALLBACK_RATES


def test_validate_conversion_rejects_unsupported_currency():
    try:
        validate_conversion(10.0, "EUR", "CHF")
    except ValueError as error:
        assert "pas prise en charge" in str(error)
    else:
        raise AssertionError("Expected ValueError")
