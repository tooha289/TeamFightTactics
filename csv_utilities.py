import csv
import json
import os
import pandas as pd

from pyparsing import Iterable


def save_csv_file(path, lines, *, mode="w", encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC):
    with open(path, mode=mode, encoding=encoding, newline="") as f:
        csv_writer = csv.writer(f, quoting=quoting)
        for line in lines:
            csv_writer.writerow(line)


def save_class_list_to_csv(
    path,
    class_list: Iterable[object],
    *,
    mode="w",
    encoding="utf-8",
    with_header=False,
    header_strip_str=None
):
    if len(class_list) < 1:
        return []
    records = [vars(instance).values() for instance in class_list]
    if with_header:
        header = [
            key.strip(header_strip_str) for key in vars(next(iter(class_list))).keys()
        ]
        records.insert(0, header)
    save_csv_file(path, records, mode=mode, encoding=encoding)


def merge_csv_files_in_directory(directory_path, encoding="utf-8", with_header=False):
    try:
        file_list = [
            file for file in os.listdir(directory_path) if file.endswith(".csv")
        ]
        header = []
        result = []

        for file_index, file in enumerate(file_list):
            full_path = os.path.join(directory_path, file)
            with open(full_path, "r", encoding=encoding) as f:
                csv_reader = csv.reader(f)

                for row_index, row in enumerate(csv_reader):
                    if with_header and file_index == 0 and row_index == 0:
                        header = row
                        continue
                    if with_header and row_index == 0:
                        continue
                    result.append(row)
        if with_header:
            result.insert(0, header)

        return result

    except Exception as e:
        print(e)
        return []


def csv_to_json(csv_file_path, json_file_path, encoding="utf-8"):
    data = []
    with open(csv_file_path, "r", newline="", encoding=encoding) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)

    with open(json_file_path, "w", encoding=encoding) as json_file:
        json.dump(data, json_file, indent=4)


def json_to_csv(json_file_path, csv_file_path, include_header=True, encoding="utf-8"):
    df = pd.read_json(json_file_path)

    df.to_csv(csv_file_path, index=False, header=include_header, encoding=encoding)


if __name__ == "__main__":
    json_file_path = r"product\results\tft_matches_20230802.json"
    csv_file_path = r"product\results\tft_matches_20230802.csv"

    json_to_csv(json_file_path, csv_file_path)
