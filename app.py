from __future__ import annotations

from datetime import datetime

import streamlit as st

from app_functions import convert

st.set_page_config(page_title="Convertisseur de devises", page_icon="💱")

st.title("Convertisseur de devises")


# Taux (temporairement codés en dur; sera remplacé en maintenance adaptative)
rates = {
    "EUR": 1,
    "USD": 1.1,
    "JPY": 130,
    "GBP": 0.86,
}

currency_list = list(rates.keys())

if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Montant :", min_value=0.0, format="%.2f")

with col2:
    st.caption("")
    from_currency = st.selectbox("De :", currency_list)
    to_currency = st.selectbox("Vers :", currency_list)

# Bouton inverser
inv_col1, inv_col2 = st.columns([1, 3])
with inv_col1:
    if st.button("⇄ Inverser"):
        st.session_state["from_currency"] = to_currency
        st.session_state["to_currency"] = from_currency

# Persist choices when inverse pressed
from_currency = st.session_state.get("from_currency", from_currency)
to_currency = st.session_state.get("to_currency", to_currency)

# Re-render consistent selections.
# (Streamlit limitation: selectbox value comes from argument)
# Conversion uses from_currency/to_currency variables.

if st.button("Convertir"):
    result = convert(amount, from_currency, to_currency, rates)
    if result is None:
        if amount <= 0:
            st.error("Le montant doit être strictement positif.")
        elif from_currency == to_currency:
            st.error("La devise source et la devise cible doivent être différentes.")

        else:
            st.error("Paramètres invalides.")
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
                "date": h["datetime"],
                "montant": h["amount"],
                "de": h["from"],
                "vers": h["to"],
                "resultat": h["result"],
            }
            for h in reversed(st.session_state.history)
        ],
        use_container_width=True,
    )
    if st.button("Vider l'historique"):
        st.session_state.history.clear()
else:
    st.info("Aucune conversion pour le moment.")
