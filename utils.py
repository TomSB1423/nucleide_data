from periodic_table import nuc
import pandas as pd


def open_data(file_dir, columns):
    """Must have Atomic Number and Mass Number"""
    # Add data to DataFrame
    df = pd.DataFrame(columns=columns)
    # Reads in data to df
    with open(file_dir, "r") as f:
        for line in f:
            stripped_line = line.strip()
            data = list(map(int, stripped_line.split(",")))
            df.loc[len(df)] = data
    # Sorts to atomic number
    df = df.sort_values(by=["Atomic Number", "Mass Number"])
    return df


def get_decay_mode(data):
    info = []
    for item in data.items():
        temp = []
        if item[0] is not None:
            temp = [item[0], item[1]["branch fraction"], item[1]["Q-value"]]
        info.append(temp)
    if info[0] == []:
        return None
    return info

def add_isotope_data(df):
    """Must have Atomic Number and Mass Number"""
    df["Symbol"] = df.apply(
        lambda x: nuc(x["Atomic Number"], x["Mass Number"])["symbol"], axis=1
    )
    df["Iso Symbol"] = df.apply(
        lambda x: nuc(x["Atomic Number"], x["Mass Number"])["symbol"]
        + " "
        + str(x["Atomic Number"])
        + "-"
        + str(x["Mass Number"]),
        axis=1,
    )
    df["Production Yield"] = df.apply(
        lambda x: x["Counts"] / df["Counts"].sum(), axis=1
    )
    df["Stable"] = df.apply(
        lambda x: nuc(x["Atomic Number"], x["Mass Number"])["stable"], axis=1
    )
    df["Half Life"] = df.apply(
        lambda x: nuc(x["Atomic Number"], x["Mass Number"])["half-life"], axis=1
    )
    df["Decay Modes (m, b, q MeV)"] = df.apply(
        lambda x: get_decay_mode(nuc(x["Atomic Number"], x["Mass Number"])["decay modes"]),
        axis=1,
    )
    df["Plot Colour"] = df.apply(lambda x: "blue" if x["Stable"] else "red", axis=1)
    return df

def print_decay_modes(Z, A):
    print(nuc(Z, A)["decay modes"])
    return