import json


def json_to_file(data, dir="./output/", file_name="data"):
    with open(dir + file_name + ".json", "w") as f:
        json.dump(data, f)


def file_to_json(dir="./output/", file_name="data"):
    try:
        with open(dir + file_name + ".json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("File Not Found")
        exit(0)
