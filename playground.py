# Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint
from periodic_table import *
import json
import os


def get_raw_data(file_dir="./assets/data.txt"):
    """Gets data from text file"""
    # Stored as: A, Z, count
    data = {}
    with open(file_dir, "r") as f:
        for line in f:
            stripped_line = line.strip()
            nums = stripped_line.split(",")
            if (int(nums[0]), int(nums[1])) in data:
                data[(int(nums[0]), int(nums[1]))] += int(nums[2])
            else:
                data[(int(nums[0]), int(nums[1]))] = int(nums[2])
    return data
    # pprint(raw_data)


def generate_isotopes(data):
    # Row: A, Z, count
    isotopes = {}
    # Used separate array to type check
    for col in data.items():
        selected_data = {}
        (
            Z,
            A,
        ) = col[0]
        counts = col[1]
        nuc_data = nuc(Z, A, E=0.0)
        symbol = nuc_data["symbol"]
        selected_data["counts"] = counts
        print(counts)
        selected_data["weight"] = str(nuc_data["weight"])
        selected_data["half-life"] = str(nuc_data["half-life"])
        selected_data["stable"] = bool(nuc_data["stable"])
        selected_data["decay modes"] = nuc_data["decay modes"]
        selected_data["mass excess"] = str(nuc_data["mass excess"])
        if nuc_data["lambda"] == float("inf"):
            selected_data["lambda"] = "inf"
        else:
            selected_data["lambda"] = float(nuc_data["lambda"])
        isotopes[f"{symbol} {Z}-{A}"] = selected_data
    return isotopes


def json_to_file(data, dir="./output/", file_name="data"):
    with open(dir + file_name + ".json", "w") as f:
        json.dump(data, f)


def file_to_json(dir="./output/", file_name="data.txt"):
    try:
        with open(dir + file_name + ".json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("File Not Found")
        exit(0)


if __name__ == "__main__":
    file_dir = "./assets/data.txt"
    raw_data = get_raw_data(file_dir)
    isotopes = generate_isotopes(raw_data)
    json_to_file(isotopes)
