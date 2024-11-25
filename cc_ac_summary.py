# Summarize month Cost Center - Account
# Source: LN Report lpbra5406m100

import os
import pandas as pd
import time
import sys
from cockpit.zrtlib import zmessage
import setup
from datetime import datetime
import warnings
import streamlit as st
import traceback


def check_args() -> bool:
    """Check if module is called with parameters needed"""
    return len(sys.argv) == 2


def create_summary(ln_file: str) -> bool:
    """"Analyze LN file passed as parameter to create new file with summary"""
    start_time = time.time()
    st.toast("Summary process starting...", icon="⚠️")
    ln_file = os.path.join(setup.input_folder, ln_file)
    if not os.path.exists(ln_file):
        zmessage(f'LN File "{ln_file}" is missing in folder "{
                 setup.input_folder}"')
        sys.exit(1)
    # --- PROCESS STARTING ----------------
    response: bool = True
    print(f'>Process starting')
    print(f'>Reading file "{ln_file}"...')
    warnings.filterwarnings("ignore")
    try:
        df = pd.read_excel(ln_file, sheet_name=setup.sheet_name)
        print(f'>File loading concluded')
        shape = df.shape
        print(f'>Table size: Rows={shape[0]} x Columns={shape[1]}')

        cols_renamed = setup.cols_names
        df.columns = cols_renamed
        print(f'>Columns names renamed')

        df['DTM_DOC'] = pd.to_datetime(df['DTM_DOC'], errors='coerce')
        df['YEAR'] = df['DTM_DOC'].dt.year
        df['MONTH'] = df['DTM_DOC'].dt.month
        print(f'>New columns YEAR and MONTH created')

        df_group = df.groupby(setup.group_by, as_index=False).agg({
            'DEBIT': 'sum', 'CREDIT': 'sum'})
        df_group['BALANCE'] = df_group['DEBIT'] - df_group['CREDIT']
        df_group['CC'] = df_group['CC'].astype('int64')
        df_group['RCD'] = datetime.now()
        df_group.reindex()
        shape = df_group.shape
        print(f'>Table size: Rows={shape[0]} x Columns={shape[1]}')

        df_group['GR'] = df_group['ACCOUNT'].astype(str).str[:5]
        df_accounts = df[['ACCOUNT', 'DESCRIPTION']].drop_duplicates()
        df_group = df_group.merge(df_accounts, on='ACCOUNT', how='left')
        df_group = df_group[setup.cols_order]

        summary_file = setup.output_folder+setup.out_file
        df_group.to_excel(summary_file, index=None, sheet_name='SUMMARY')
        print(f'>Summary file "{summary_file}" created')
    except Exception as e:
        st.toast(f'🚨 There was a critical error', icon="🚨")
        st.error("An error occurred. Check the logs for more details.")
        # Muestra el traceback completo en la página
        st.text(traceback.format_exc())
        zmessage(f'Critical error: {e}', 'e')
        response = False
    end_time = time.time()
    lapse_seconds = int(round(end_time-start_time, 0))
    print(f'>Process executed in {lapse_seconds} seconds')
    return response


if __name__ == '__main__':
    if check_args():
        if create_summary(sys.argv[1]):
            print(f'>Process concluded successfully!!!')
    else:
        zmessage('LN file not defined!!!')
