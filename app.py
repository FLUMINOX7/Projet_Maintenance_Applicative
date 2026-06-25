import streamlit as st

from app_functions import SUPPORTED_CURRENCIES, convert_currency


st.title("Convertisseur de devises")

amount = st.number_input("Montant :", min_value=0.0, format="%.2f")
from_currency = st.selectbox("De :", SUPPORTED_CURRENCIES)
to_currency = st.selectbox("Vers :", SUPPORTED_CURRENCIES)

if st.button("Convertir"):
    try:
        result = convert_currency(amount, from_currency, to_currency)
    except ValueError as error:
        st.error(str(error))
    else:
        st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")