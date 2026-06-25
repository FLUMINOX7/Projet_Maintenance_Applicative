from __future__ import annotations

from datetime import datetime

import streamlit as st

from app_functions import SUPPORTED_CURRENCIES, convert_currency


st.set_page_config(page_title="Convertisseur de devises", page_icon="💱", layout="centered")

st.title("Convertisseur de devises")
st.caption("Maintenance corrective, évolutive, adaptative et perfective réunies dans une seule version.")


if "history" not in st.session_state:
    st.session_state.history = []

if "from_currency" not in st.session_state:
    st.session_state.from_currency = SUPPORTED_CURRENCIES[0]

if "to_currency" not in st.session_state:
    st.session_state.to_currency = SUPPORTED_CURRENCIES[1]


amount_col, currency_col = st.columns([1, 1])

with amount_col:
    amount = st.number_input("Montant :", min_value=0.0, format="%.2f", step=0.01)

with currency_col:
    st.selectbox("De :", SUPPORTED_CURRENCIES, key="from_currency")
    st.selectbox("Vers :", SUPPORTED_CURRENCIES, key="to_currency")


button_col_1, button_col_2 = st.columns(2)

with button_col_1:
    swap_pressed = st.button("⇄ Inverser", use_container_width=True)

with button_col_2:
    convert_pressed = st.button("Convertir", use_container_width=True)


if swap_pressed:
    st.session_state.from_currency, st.session_state.to_currency = (
        st.session_state.to_currency,
        st.session_state.from_currency,
    )
    st.rerun()


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
