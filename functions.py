# FUNCTIONS FILE -----------------------------
import xlwings as xw
import os
import setup


def file_is_ok(lnreport: str) -> str:
    """
    Check if file passed as parameter is right to be analyzed to create summary
    Args:
        ln_report (str): LN Report filename including path
    Return:
        str: Empty string if file is right, otherwise string with error description
    """
    # --- SETUP VARIABLES ------------
    response = True
    wb_opened = False
    ln_program = setup.check_xls_values['ln_program']
    sheet = setup.check_xls_values['sheet_name']
    cols_num = setup.check_xls_values['cols_num']
    cols_ok = setup.check_xls_values['cols_ok']
    msg = ''
    if response and not os.path.exists(lnreport):
        msg = f'File "{lnreport}" is missing'
        response = False
    file_ext = '.xlsx'
    if response and not os.path.basename(lnreport).endswith(file_ext):
        msg = f'File has no extension "{file_ext}" needed'
        response = False
    if response and os.path.basename(lnreport)[:len(ln_program)] != ln_program:
        msg = f'Wrong LN file. Filename must start as "{ln_program}..."'
        response = False
    if response:
        try:
            app = xw.App(visible=False)
            wb = app.books.open(lnreport)
            wb_sheets = [sheet.name for sheet in wb.sheets]
            wb_opened = True
        except Exception as e:
            response = False
            msg = f'xlwings error: {e}'
    if response and sheet not in wb_sheets:
        msg = f'Sheet "{sheet}" is missing'
        response = False
    if response:
        sht = wb.sheets[sheet]
        cols = sht.range((1, 1), (1, cols_num)).value
        if not cols == cols_ok:
            msg = f'File columns are not right!'
            response = False
    if wb_opened:
        wb.close()
        app.quit()
    print(f'file_is_ok() => "{msg}"')
    return msg
