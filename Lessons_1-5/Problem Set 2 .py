### Lesson 2

from bs4 import BeautifulSoup
import requests
import json

html_page = "page_source.html"


def extract_data(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    with open(page, "r") as html:
        soup = BeautifulSoup(html, "lxml")
        e = soup.find(id = "__EVENTVALIDATION")
        data["eventvalidation"] = e["value"]
        v = soup.find(id = "__VIEWSTATE")
        data["viewstate"] = v["value"]
        pass

    return data

data = extract_data(html_page)

def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': "BOS",
                          'CarrierList': "VX",
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text

make_request(data)


### Problem Set 2.1
from bs4 import BeautifulSoup
html_page = "options.html"


def extract_carriers(page):
    data = []

    with open(page, "r") as html:
        soup = BeautifulSoup(html, "lxml")
        CL = soup.find(id = "CarrierList")
        for i in CL.find_all('option'):
            data.append(i["value"])
            
    return data[3:]

print extract_carriers(html_page)

def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]
    airport = data["airport"]
    carrier = data["carrier"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': airport,
                          'CarrierList': carrier,
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text
   
### Problem Set 2.3
   from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files


def process_file(f):
    
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-")
    
    with open("{}/{}".format(datadir, f), "r") as html:
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table", {"class":"dataTDRight"})
        tr = table.find_all("tr")
        for i in tr:
            col = i.find_all("td")
            cols = [row.text.strip().replace(',','') for row in col]
            if "TOTAL" in cols:
                continue
            else:
                if cols[0].isdigit():
                    info["year"] = int(cols[0])
                if cols[1].isdigit():
                    info["month"] = int(cols[1])
                if cols[2].isdigit() and cols[3].isdigit():
                    flight = {}
                    flight["domestic"] = int(cols[2])
                    flight["international"] = int(cols[3])
                    info["flights"] = flight
            
            data.append(info)
            
        return data
        
### Prolem Set 2.6 
def split_file(filename):
    # we want you to split the input file into separate files
    # each containing a single patent.
    # As a hint - each patent declaration starts with the same line that was causing the error
    # The new files should be saved with filename in the following format:
    # "{}-{}".format(filename, n) where n is a counter, starting from 0.
    with open(filename, 'r') as f:
        patents = []
        data = f.read()
        lines = data.splitlines()
        n = 0
        for line in lines:
            ### open and write file 
            if line == '''<?xml version="1.0" encoding="UTF-8"?>''':
                newfile = open('{}-{}'.format(filename, n), 'w')
                newfile.write(line)
                n += 1
            ### close file before next <?xml
            elif line == '''</us-patent-grant>''':
                newfile.write(line)
                patents.append(newfile)
                newfile.close()
            else: 
                newfile.write(line)
                
        print patents
    