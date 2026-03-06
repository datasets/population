import csv
import os
import tempfile
import zipfile

import requests


def download():
    source = "http://api.worldbank.org/countries/all/indicators/SP.POP.TOTL?downloadformat=csv"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmpfile:
        response = requests.get(source)
        response.raise_for_status()
        tmpfile.write(response.content)
        archive_path = tmpfile.name

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(tmpdir)

            for root, _, files in os.walk(tmpdir):
                for name in files:
                    if name.startswith("API_SP.POP.TOTL_DS2_") and name.endswith(
                        ".csv"
                    ):
                        output_path = os.path.join("data", "population.csv")
                        process(os.path.join(root, name), output_path)
                        return
    finally:
        os.unlink(archive_path)

    raise FileNotFoundError("Could not find population CSV in downloaded archive")


def process(filename, output_path):
    with open(filename) as fo:
        lines = [row for row in csv.reader(fo)]
    headings = lines[4]
    lines = lines[5:]

    outheadings = ["Country Name", "Country Code", "Year", "Value"]
    outlines = []

    for row in lines:
        for idx, year in enumerate(headings[4:]):
            if row[idx + 4]:
                value = row[idx + 4]
                outlines.append(row[:2] + [int(year), value])

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(outheadings)
        writer.writerows(outlines)


if __name__ == "__main__":
    download()
