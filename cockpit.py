import streamlit as st
import pandas as pd
import os
from cc_ac_summary import create_summary
from zrtlib import JSON_load
import setup

# Configure the Streamlit page
st.set_page_config(page_title="Cockpit :: LN Data", layout="centered")

# Session variables initialization
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
if 'new_file_created' not in st.session_state:
    st.session_state.new_file_created = False


# Title and subheader
st.title("📈 AUNDE Cockpit")
st.subheader("Cost Center and Account summary")
st.write('---')

# File upload with clear instructions
uploaded_file = st.file_uploader(
    "Select LN file with data extracted (XLSX format)", type=["xlsx"]
)

# Processing logic with progress bar and feedback
if uploaded_file:
    with st.spinner("Uploading your file..."):
        with open(f"{setup.input_folder}{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_path = f.name
        saved_path = os.path.abspath(saved_path)
        st.session_state.file_uploaded = True
else:
    st.info("⚠️ Please upload an XLSX file to continue...")

# Activate summary creation button
if st.session_state.file_uploaded:
    with st.spinner("Processing your file..."):
        if st.button("⚙️ Create summary file"):
            if create_summary(saved_path):
                st.session_state.new_file_created = True
                st.info(f'👌 Summary file created!')
            else:
                st.warning(f'🚨 There was a problem to create summary')

# Download new file created
if st.session_state.file_uploaded and st.session_state.new_file_created:
    # Check if summary file exists
    summary_path = os.path.join(setup.output_folder, setup.out_file)
    if os.path.exists(summary_path):
        with open(summary_path, "rb") as f:
            summary_data = f.read()
        download_button = st.download_button(
            label="📥 Download Summary",
            data=summary_data,
            file_name=setup.out_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        if download_button:
            st.success(f' Summary file downloaded!')
    else:
        st.warning(f' Summary file not found at {summary_path}')
