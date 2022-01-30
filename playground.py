# Imports
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from pprint import pprint
import copy

# Module imports
from periodic_table import *
from utils import json_to_file, file_to_json


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


def plot_hist(data):
    n, labels, counts, colors = [], [], [], []
    temp_symbol = ""
    # Counter for y axis
    i = 0
    for isotope, info in data.items():
        n.append(i)
        # Omits labels of same element as to not clutter y axis
        isotope = isotope.split(" ")[0]
        if isotope not in temp_symbol:
            labels.append(isotope)
            temp_symbol = isotope
        else:
            labels.append("")

        # Color for un/stable
        if info["stable"]:
            colors.append("blue")
        else:
            colors.append("red")
        counts.append(info["counts"])
        i += 1
    # Plotting
    fig, ax = plt.subplots()
    ax.barh(n, counts, log=True, color=colors)
    ax.set_yticks(np.arange(len(n)))
    ax.set_yticklabels(labels)
    plt.tight_layout()
    red_patch = mpatches.Patch(color="red", label="Unstable")
    blue_patch = mpatches.Patch(color="blue", label="Stable")
    ax.legend(handles=[red_patch, blue_patch], loc=0)
    plt.show()


def filter_stable(data):
    new_data = data.copy()
    for isotope, info in data.items():
        if info["stable"]:
            new_data.pop(isotope)
    return new_data


if __name__ == "__main__":
    # file_dir = "./assets/data.txt"
    # raw_data = get_raw_data(file_dir)
    # isotopes = generate_isotopes(raw_data)
    # json_to_file(isotopes)
    isotopes = file_to_json()
    plot_hist(isotopes)
    isotopes = filter_stable(isotopes)
    plot_hist(isotopes)
