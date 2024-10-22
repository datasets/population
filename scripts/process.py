import requests
import os
import csv
import tempfile
import zipfile

tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
tmpdir = tempfile.TemporaryDirectory()

def download():

    global filename
    
    source = 'http://api.worldbank.org/countries/all/indicators/SP.POP.TOTL?downloadformat=csv'
    
    response = requests.get(source)
    with open(tmpfile.name, 'wb') as d:
        d.write(response.content)
    
    with zipfile.ZipFile(tmpfile.name, 'r') as zip_ref:
        zip_ref.extractall(tmpdir.name)
    
    os.unlink(tmpfile.name)
    
    for path in os.scandir(tmpdir.name):
        if path.is_file():
            if path.name.startswith('API_SP.POP.TOTL_DS2_EN'):
                filename = os.path.join(tmpdir.name, path.name)

def process():
    global filename
    with open(filename) as fo:
        lines = [row for row in csv.reader(fo)]
    headings = lines[4]
    lines = lines[5:]
    
    outheadings = ['Country Name', 'Country Code', 'Year', 'Value']
    outlines = []

    for row in lines:
        for idx, year in enumerate(headings[4:]):
            if row[idx+4]:
                value = row[idx+4]
                outlines.append(row[:2] + [int(year), value])

    with open('data/population.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(outheadings)
        writer.writerows(outlines)

if __name__ == '__main__':
    download()
    process()
