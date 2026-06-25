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
