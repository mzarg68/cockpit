# PYTHON MODULE TO SUPPORT COCKPIT DATA

import streamlit as st
import pandas as pd
import os

# Configurar la página de Streamlit
st.set_page_config(page_title="Cockpit :: XLSX files", layout="centered")

# Título de la aplicación
st.title("📊 AUNDE Cockpit")
st.subheader("Cost Center and Account data")
st.write('---')

# Subir archivo Excel
uploaded_file = st.file_uploader(
    "Select LN file with data extracted", type=["xlsx"])

# Verificar si el archivo ha sido subido
if uploaded_file:
    with open(f"./temp/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
        saved_path = f.name
    saved_path = os.path.abspath(saved_path)
    st.info(f"File '{uploaded_file.name}' saved in {
            os.path.dirname(saved_path)}")
    if st.button("⚙️ Get summary file"):
        pass
else:
    st.info("⚠️ Please upload file to continue...")
