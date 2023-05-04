import urllib.request
import os
import csv
import tempfile
import zipfile

tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
tmpdir = tempfile.TemporaryDirectory()

def download():

    global filename
    
    source = 'http://api.worldbank.org/countries/all/indicators/SP.POP.TOTL?downloadformat=csv'
    
    with urllib.request.urlopen(source) as response:
        with open(tmpfile.name, mode="wb") as d:
            d.write(response.read())
            tmpfile.close()
    
    with zipfile.ZipFile(tmpfile.name, 'r') as zip_ref:
        zip_ref.extractall(tmpdir.name)
        tmpfile.close()
        os.unlink(tmpfile.name)
    
    for path in os.scandir(tmpdir.name):
        if path.is_file():
            #print(path.name)
            if path.name.startswith('API_SP.POP.TOTL_DS2_EN'):
                filename = tmpdir.name + '/' + path.name
            
def process():
    # un-pivot the table
    global filename
    fo = open(filename)
    lines = [ row for row in csv.reader(fo) ]
    headings = lines[4]
    lines = lines[5:]
    
    outheadings = [ 'Country Name', 'Country Code', 'Year', 'Value' ]
    outlines = []

    for row in lines:
        for idx, year in enumerate(headings[4:]):
            if row[idx+4]:
                # do not convert to float as we end up with scientific notation
                value = row[idx+4]
                outlines.append(row[:2] + [int(year), value])

    writer = csv.writer(open('data/population.csv', 'w'))
    writer.writerow(outheadings)
    writer.writerows(outlines)

download()
process()
