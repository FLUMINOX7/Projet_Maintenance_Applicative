from __future__ import annotations

import os
from datetime import datetime

import streamlit as st

from app_functions import API_KEY_ENV_VAR, SUPPORTED_CURRENCIES, convert_currency


st.set_page_config(page_title="Convertisseur de devises", layout="centered")

st.title("Convertisseur de devises")


if "history" not in st.session_state:
    st.session_state.history = []

if "feedback_message" not in st.session_state:
    st.session_state.feedback_message = ""

if "feedback_kind" not in st.session_state:
    st.session_state.feedback_kind = "info"

if "from_currency" not in st.session_state:
    st.session_state.from_currency = SUPPORTED_CURRENCIES[0]

if "to_currency" not in st.session_state:
    st.session_state.to_currency = SUPPORTED_CURRENCIES[1]


def swap_currencies() -> None:
    st.session_state.from_currency, st.session_state.to_currency = (
        st.session_state.to_currency,
        st.session_state.from_currency,
    )
    st.session_state.feedback_kind = "info"
    st.session_state.feedback_message = "Les devises ont été inversées."


amount_col, currency_col = st.columns([1, 1])

if st.session_state.feedback_message:
    feedback = st.session_state.feedback_message
    feedback_kind = st.session_state.feedback_kind
    st.session_state.feedback_message = ""
    st.session_state.feedback_kind = "info"
    if feedback_kind == "error":
        st.error(feedback)
    elif feedback_kind == "success":
        st.success(feedback)
    else:
        st.info(feedback)

with amount_col:
    amount = st.number_input("Montant :", min_value=0.0, format="%.2f", step=0.01)

with currency_col:
    st.selectbox("De :", SUPPORTED_CURRENCIES, key="from_currency")
    st.selectbox("Vers :", SUPPORTED_CURRENCIES, key="to_currency")


button_col_1, button_col_2 = st.columns(2)

with button_col_1:
    st.button("⇄ Inverser", use_container_width=True, on_click=swap_currencies)

with button_col_2:
    convert_pressed = st.button("Convertir", use_container_width=True)


if convert_pressed:
    from_currency = st.session_state.from_currency
    to_currency = st.session_state.to_currency

    try:
        result = convert_currency(amount, from_currency, to_currency)
    except ValueError as error:
        st.error(str(error))
    else:
        st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
        st.session_state.history.append(
            {
                "datetime": datetime.now().isoformat(timespec="seconds"),
                "amount": float(amount),
                "from": from_currency,
                "to": to_currency,
                "result": float(result),
            }
        )


st.subheader("Historique")

if st.session_state.history:
    st.dataframe(
        [
            {
                "date": item["datetime"],
                "montant": item["amount"],
                "de": item["from"],
                "vers": item["to"],
                "resultat": item["result"],
            }
            for item in reversed(st.session_state.history)
        ],
        use_container_width=True,
    )

    if st.button("Vider l'historique"):
        st.session_state.history.clear()
        st.rerun()
else:
    st.info("Aucune conversion pour le moment.")
