import tempfile
import os
import csv
import io
import zipfile
import pandas as pd
from budgewiser.project import estimation


def generate_report(data):
    files = []
    with tempfile.TemporaryDirectory() as tempdir:
        # Create a temporary directory to store the files
        # Generate the report files

        # save project info as csv file in the tempdir
        meta_input = data.get("meta_input", {})
        meta_input_path = os.path.join(tempdir, "meta_input.csv")
        with open(meta_input_path, "w") as f:
            w = csv.DictWriter(f, meta_input.keys())
            w.writeheader()
            w.writerow(meta_input)

        # save estimation_input as csv file in the tempdir
        estimation_input = data.get("estimation_input", {})
        estimation_input_path = os.path.join(tempdir, "estimation_input.csv")
        with open(estimation_input_path, "w") as f:
            w = csv.DictWriter(f, estimation_input.keys())
            w.writeheader()
            w.writerow(estimation_input)

        # save estimation_output as csv file in the tempdir
        estimation_output = data.get("estimation_output", {})
        estimation_output_path = os.path.join(tempdir, "estimation_output.csv")
        with open(estimation_output_path, "w") as f:
            w = csv.DictWriter(f, estimation_output.keys())
            w.writeheader()
            w.writerow(estimation_output)

        # After each file is saved, read it into memory and add it to the files list
        for root, dirs, file_names in os.walk(tempdir):
            for file_name in file_names:
                file_path = os.path.join(root, file_name)
                with open(file_path, "rb") as f:
                    data = f.read()
                files.append((file_name, data))

    in_memory_output = io.BytesIO()
    with zipfile.ZipFile(in_memory_output, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_name, data in files:
            data = data.encode() if isinstance(data, str) else data
            data = io.BytesIO(data)
            zf.writestr(file_name, data.getvalue())

    in_memory_output.seek(0)

    return in_memory_output
