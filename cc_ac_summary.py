# Summarize month Cost Center - Account
# Source: LN Report lpbra5406m100

import os
import pandas as pd
import time
import sys
from zrtlib import msg_warning as warning, JSON_load


def check_args() -> bool:
    """Check if module is called with parameters needed"""
    return len(sys.argv) == 2


def main(json_file: str) -> None:
    """"Analyze LN file passed as parameter to create new file with summary"""
    start_time = time.time()
    if not os.path.exists(json_file):
        warning(f'LN parameters file "{json_file}" is missing!')
        sys.exit(1)
    param = JSON_load(json_file)
    ln_file = os.path.join(param['input_folder'], param['ln_filename'])
    if not os.path.exists(ln_file):
        print(f'File "{ln_file}" is missing')
        sys.exit(1)
    # --- PROCESS STARTING ----------------
    print(f'>Process starting')
    print(f'>Reading file "{ln_file}"...')
    df = pd.read_excel(ln_file, sheet_name=param['xlsx_sheet'])
    print(f'>File loading concluded')
    shape = df.shape
    print(f'>Table size: Rows={shape[0]} x Columns={shape[1]}')

    cols_renamed = param['cols_names']
    df.columns = cols_renamed
    print(f'>Columns names renamed')

    df['DTM_DOC'] = pd.to_datetime(df['DTM_DOC'], errors='coerce')
    df['YEAR'] = df['DTM_DOC'].dt.year
    df['MONTH'] = df['DTM_DOC'].dt.month
    print(f'>New columns YEAR and MONTH created')

    df_group = df.groupby(param['group_by'], as_index=False).agg({
        'DEBIT': 'sum', 'CREDIT': 'sum'})
    df_group['BALANCE'] = df_group['DEBIT'] - df_group['CREDIT']
    df_group['CC'] = df_group['CC'].astype('int64')
    df_group.reindex()
    shape = df_group.shape
    print(f'>Table size: Rows={shape[0]} x Columns={shape[1]}')

    summary_file = param['output_folder']+param['output_filename']
    df_group.to_excel(summary_file, index=None, sheet_name='SUMMARY')
    print(f'>Summary file "{summary_file}" created')

    end_time = time.time()
    lapse_seconds = int(round(end_time-start_time, 0))
    print(f'>Process executed in {lapse_seconds} seconds')


if __name__ == '__main__':
    if check_args():
        main(sys.argv[1])
    else:
        warning('LN file parameters not defined')
