import urllib
import os
import csv
import tempfile

f = tempfile.NamedTemporaryFile()
dest = f.name

def download():
    source = 'http://api.worldbank.org/countries/all/indicators/SP.POP.TOTL?format=csv'
    urllib.urlretrieve(source, dest)

def process():
    # un-pivot the table
    fo = open(dest)
    lines = [ row for row in csv.reader(fo) ]
    headings = lines[0]
    lines = lines[1:]

    outheadings = [ 'Country Name', 'Country Code', 'Year', 'Value' ]
    outlines = []

    for row in lines:
        for idx, year in enumerate(headings[2:]):
            if row[idx+2]:
                # do not convert to float as we end up with scientific notation
                value = row[idx+2]
                outlines.append(row[:2] + [int(year), value])

    writer = csv.writer(open('data/population.csv', 'w'))
    writer.writerow(outheadings)
    writer.writerows(outlines)

download()
process()
