# Z LIBRARY TO BE USED FOR ANY PROJECT
import os
import platform
import json
from datetime import datetime


def FolderExists(folder: str = "") -> bool:
    """Define if folder passed as parameter exists or not"""
    return os.path.exists(folder) and os.path.isdir(folder)


def FileExists(file: str = "") -> bool:
    """Define if file passed as parameter exists or not"""
    return os.path.exists(file) and os.path.isfile(file)


def JSON_load(Filename: str) -> dict:
    """Load JSON filename passed as parameter and return a dictionary"""
    prm = {}
    if os.path.exists(Filename) and os.path.isfile(Filename):
        with open(Filename, "r") as f:
            prm = json.load(f)
    else:
        print(f">JSON file {Filename} is missing")
    return prm


def JSON_save(data: dict, Filename: str) -> bool:
    """Save a dictionary to a file with the specified filename in JSON format."""
    try:
        # Write the dictionary to a JSON file
        with open(Filename, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"> An error occurred: {e}")
        return False


def JSON_converter(infile: str, jsonfile: str, indent: int = 2) -> None | str:
    """Convert input filename to json file and save it on same folder"""
    if not os.path.exists(infile):
        print(f'File <{infile}> is missing!')
        return None
    folder = os.path.dirname(infile)
    if os.path.dirname(jsonfile) == '':
        jsonfile = os.path.join(folder, jsonfile)
    else:
        if not os.path.exists(os.path.dirname(jsonfile)):
            os.makedirs(os.path.dirname(jsonfile))
    with open(infile, "r", encoding='utf-8') as f:
        prm = f.read()
    data = json.loads(prm)
    with open(jsonfile, "w") as f:
        json.dump(data, f, indent=indent, sort_keys=True)
    print(f"JSON file created -> {jsonfile}")


def msg_warning(text: str) -> None:
    """Print a warning message to console"""
    width = 20
    if len(text) > width:
        width = len(text)+2
    line = "WARNING".center(width, "*")
    print(line)
    print(f'>{text}')
    print(f'>{datetime.now():%Y-%m-%d %H:%M}')
    print("".center(width, "*"))


def get_download_folder():
    """Return current chrome download folder (code suggested by you.com)"""
    system = platform.system()
    user_folder = os.path.expanduser("~")
    if system == "Windows":
        return os.path.join(user_folder, "Downloads")
    elif system == "Darwin":  # macOS
        return os.path.join(user_folder, "Downloads")
    elif system == "Linux":  # Linux
        return os.path.join(user_folder, "Descargas")
    else:
        return None


if __name__ == "__main__":
    filename = os.path.basename(__file__)
    text = f'This file "{filename}" is a library of functions'
    print(len(text)*'*')
    print(text)
    print(len(text)*'*')
