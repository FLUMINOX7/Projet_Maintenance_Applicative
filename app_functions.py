from __future__ import annotations

import os
from typing import Mapping

import requests


BASE_RATES = {
    "EUR": 1.0,
    "USD": 1.1,
    "JPY": 130.0,
    "GBP": 0.86,
    "CAD": 1.47,
}
SUPPORTED_CURRENCIES = tuple(BASE_RATES.keys())
API_URL_TEMPLATE = "https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
API_KEY_ENV_VAR = "EXCHANGERATE_API_KEY"


def validate_conversion(amount: float, from_currency: str, to_currency: str) -> None:
    if amount <= 0:
        raise ValueError("Le montant doit être strictement positif.")

    if from_currency == to_currency:
        raise ValueError("La devise source et la devise cible doivent être différentes.")

    if from_currency not in SUPPORTED_CURRENCIES or to_currency not in SUPPORTED_CURRENCIES:
        raise ValueError("Une devise sélectionnée n'est pas prise en charge.")


def _build_rate_table(base_currency: str, reference_rates: Mapping[str, float] = BASE_RATES) -> dict[str, float]:
    base_rate = reference_rates[base_currency]
    return {
        currency: rate / base_rate
        for currency, rate in reference_rates.items()
    }


def fetch_rates(
    base_currency: str,
    api_key: str | None = None,
    timeout: int = 10,
) -> dict[str, float]:
    resolved_api_key = (api_key or os.getenv(API_KEY_ENV_VAR, "")).strip()

    if resolved_api_key:
        try:
            response = requests.get(
                API_URL_TEMPLATE.format(api_key=resolved_api_key, base_currency=base_currency),
                timeout=timeout,
            )
            response.raise_for_status()
            data = response.json()

            if data.get("result") != "success":
                error_message = data.get("error-type") or "Impossible de récupérer les taux de change."
                raise ValueError(error_message)

            raw_rates = data.get("conversion_rates", {})
            rates = {
                currency: float(raw_rates[currency])
                for currency in SUPPORTED_CURRENCIES
                if currency in raw_rates
            }

            if len(rates) == len(SUPPORTED_CURRENCIES):
                return rates
        except (requests.RequestException, TypeError, ValueError):
            pass

    return _build_rate_table(base_currency)


def convert(
    amount: float,
    from_currency: str,
    to_currency: str,
    rates: Mapping[str, float],
) -> float | None:
    if amount <= 0:
        return None

    if from_currency == to_currency:
        return None

    try:
        return amount * rates[to_currency] / rates[from_currency]
    except KeyError:
        return None


def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
    api_key: str | None = None,
) -> float:
    validate_conversion(amount, from_currency, to_currency)
    rates = fetch_rates(from_currency, api_key=api_key)
    result = convert(amount, from_currency, to_currency, rates)

    if result is None:
        raise ValueError("Conversion impossible avec les taux disponibles.")

    return result
