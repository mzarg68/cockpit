import streamlit as st
import os
from cc_ac_summary import create_summary
import setup
import time
from functions import file_is_ok as fok

# Configuración inicial de la página
st.set_page_config(page_title="Cockpit :: LN Data", layout="centered")

# Inicialización de variables de sesión
if 'step' not in st.session_state:
    st.session_state.step = 1  # Paso inicial
if 'file_path' not in st.session_state:
    st.session_state.file_path = None
if 'summary_created' not in st.session_state:
    st.session_state.summary_created = False

# Títulos de la app
st.title("📈 AUNDE Cockpit")
st.subheader("Cost Center and Account Summary")
st.markdown(f"<small>{setup.app_version} {
            setup.app_release} by mzarate©️</small>", unsafe_allow_html=True)
st.write('---')

# Función para reiniciar el proceso


def restart_process():
    st.session_state.step = 1
    st.session_state.file_path = None
    st.session_state.summary_created = False


# Paso 1: Subir el archivo
if st.session_state.step == 1:
    st.header("Step 1/4: Upload LN file")
    st.info("⚠️ Please upload XLSX file to continue...")
    uploaded_file = st.file_uploader(
        "Select LN file - Program lpbra5406 (XLSX format)", type=["xlsx"]
    )
    if uploaded_file:
        with open(f"{setup.input_folder}{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.file_path = os.path.abspath(f.name)
        st.session_state.step = 2  # Avanza al paso 2
        st.rerun()

# Paso 2: Procesar el archivo
elif st.session_state.step == 2:
    st.header("Step 2/4: Summary creation")
    st.success(f'File "{os.path.basename(
        st.session_state.file_path)}" uploaded successfully')
    st.info("ℹ️ Press START to run process")
    col1, col2, col3 = st.columns([2, 2, 3])
    check_msg = ''
    error_msg = ''
    with col1:
        if st.button("⚙️ START"):
            start_time = time.time()
            with st.spinner("Checking file..."):
                check_msg = fok(st.session_state.file_path)
            if check_msg == '':
                with st.spinner("Processing file..."):
                    if create_summary(st.session_state.file_path):
                        st.session_state.summary_created = True
                        st.session_state.step = 3  # Avanza al paso 3
                        end_time = time.time()
                        lapse_seconds = int(round(end_time-start_time, 0))
                        st.session_state.lapse = lapse_seconds
                        st.rerun()
                    else:
                        error_msg = "🚨 There was a problem to create summary file"
            else:
                error_msg = f"🚨 {check_msg}"
    with col2:
        if st.button("🔄 RESTART"):
            restart_process()
            st.rerun()
    if error_msg != '':
        st.error(error_msg)


# Paso 3: Descargar el archivo creado
elif st.session_state.step == 3:
    st.header("Step 3/4: Download summary file")
    st.success(f'File "{setup.out_file}" created successfully in {
               st.session_state.lapse} seconds')
    st.info("ℹ️ Press DOWNLOAD to get summary file created")
    col1, col2, col3 = st.columns([2, 2, 3])
    summary_path = os.path.join(setup.output_folder, setup.out_file)
    if os.path.exists(summary_path):
        with open(summary_path, "rb") as f:
            summary_data = f.read()
        with col1:
            st.download_button(
                label="📥 DOWNLOAD",
                data=summary_data,
                file_name=setup.out_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            st.session_state.step = 4  # Avanza al paso 3
        with col2:
            if st.button("🔄 RESTART"):
                restart_process()
                st.rerun()
    else:
        st.warning(f"Summary file not found at {summary_path}")
        if st.button("🔄 Restart"):
            restart_process()
            st.rerun()

# Paso 4: Finalizar y reiniciar el proceso
elif st.session_state.step == 4:
    st.header("Step 4/4: Restart process")
    st.success(f'🎉 File "{setup.out_file}" downloaded successfully')
    if st.button("🔄 RESTART"):
        restart_process()
        st.rerun()
