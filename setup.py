# COCKPIT SETUP
import os
import sys
from zrtlib import zmessage, JSON_load

config_file = 'cockpit.json'
if not os.path.exists(config_file):
    zmessage(f'Cockpit config file "{config_file}" is missing!')
    sys.exit(1)
prm = JSON_load(config_file)
input_folder = prm['input_folder']
output_folder = prm['output_folder']
if not os.path.exists(input_folder):
    os.makedirs(input_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
sheet_name = prm['xlsx_sheet']
out_file = prm['output_filename']
cols_names = prm['cols_names']
group_by = prm['group_by']
