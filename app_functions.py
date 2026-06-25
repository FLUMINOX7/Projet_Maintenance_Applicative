import requests


SUPPORTED_CURRENCIES = ("EUR", "USD", "JPY")
API_KEY = "6563bd1f49f6d2bbf06c92d7"
API_URL_TEMPLATE = "https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"


def validate_conversion(amount, from_currency, to_currency):
    if amount <= 0:
        raise ValueError("Le montant doit être strictement positif.")

    if from_currency == to_currency:
        raise ValueError("La devise source et la devise cible doivent être différentes.")


def fetch_rates(base_currency):
    response = requests.get(
        API_URL_TEMPLATE.format(api_key=API_KEY, base_currency=base_currency),
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    if data.get("result") != "success":
        error_message = data.get("error-type") or "Impossible de récupérer les taux de change."
        raise ValueError(error_message)

    return data.get("conversion_rates", {})


def convert_currency(amount, from_currency, to_currency):
    validate_conversion(amount, from_currency, to_currency)
    rates = fetch_rates(from_currency)

    if to_currency not in rates:
        raise ValueError("La devise cible n'est pas disponible via l'API.")

    return amount * rates[to_currency]
from __future__ import annotations

from typing import Mapping


def convert(
    amount: float,
    from_currency: str,
    to_currency: str,
    rates: Mapping[str, float],
) -> float | None:
    """Convert an amount from one currency to another.

    Returns:
        The converted amount, or None if inputs are invalid.
    """

    if amount <= 0:
        return None

    if from_currency == to_currency:
        return None

    return amount * rates[to_currency] / rates[from_currency]
