# performs clean up

import os
import re
from aboip1.views.inputs import Inputs
from aboip1.views.logging import getLogger
from flask import session

logger = getLogger()

# pattern = r"results-row\d+-row\d+.csv"
pattern = r"results-row\d+-row\d+-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\.csv"

file_list = []

current_directory = os.path.dirname(os.path.abspath(__file__))
result_dir = os.path.join(current_directory, "results")
os.makedirs(result_dir, exist_ok=True)


def list_files():
    global file_list
    file_list = []
    for filename in os.listdir(result_dir):
        # print(filename)
        # if re.match(pattern, filename):
        # print('match found', filename)
        if not os.path.isfile(os.path.join(result_dir, filename)):
            continue
        if re.match(pattern, filename):
            file_list.append(filename)
        if filename == "latest_j.txt":
            file_list.append(filename)
    return file_list


def cleanup():
    print(file_list)
    try:
        if len(file_list):
            for filename in file_list:
                os.remove(os.path.join(result_dir, filename))
            Inputs.flag = 1
            return 1
        Inputs.flag = 0
        return 0
    except FileNotFoundError:
        print("File not present")


def getFilePath(file_identifier):
    logger.debug(f"unique_identifier in helper.py: {file_identifier}")
    file_list = list_files()
    for file in file_list:
        if file.find(file_identifier) != -1:
            return os.path.join(result_dir, file)
    return None
