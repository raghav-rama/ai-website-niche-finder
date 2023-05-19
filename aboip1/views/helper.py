# performs clean up

import os
import re

pattern = r"results-row\d+-row\d+.csv"

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


def cleanup():
    # s = input("type 'yes' if you want to remove output file: ")
    # if s == 'yes':
    print(file_list)
    try:
        if len(file_list):
            s = input("Found older result files, cleanup? y/n: ")
            if s == "y":
                for filename in file_list:
                    os.remove(os.path.join(result_dir, filename))
                return 1
            else:
                print("cool")
                return 0
    except FileNotFoundError:
        print("File not present")
