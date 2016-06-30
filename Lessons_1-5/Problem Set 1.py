### Lession 1 

### fields = columns ; item = rows ; value = cell 
import os 
import csv 

def parse_file (df):
    data = []
    with open(str(df), "r") as f: 
        header = f.readline().split(',')
        counter = 0
        for line in f: 
            if counter == 10:
                break 
            
            fields = line.split(',')
            entry = {}
            
            for i, value in enumerate(fields):
                entry[header[i].strip()] = value.strip()
                
            data.append(entry)
            counter += 1
        
    return data 

### Lession 1.11    
import xlrd 
from zipfile import ZipFile

### other useful meathods: 
print sheet.nrows
print sheet.ncols
print sheet.cell_type(3,2)
#(row_input, col_input)
print sheet.cell_value(3,2)
#(specify which col or row, start, stop)
print sheet.col_values(3, start_rowx=1, end_rowx=4)
header = sheet.row_values(0, start_colx=0, end_colx=10)
print exeltime = sheet.cell_value(1,0)
print xlrd.xldate_as_tuple(exceltime,0)

def open_zip(df):
    with ZipFile('{0}'.format(df), 'r') as myzip:
        myzip.extractall()
        
def parse_file(df):
    workbook = xlrd.open_workbook(df)
    sheet = workbook.sheet_by_index(0)
    #all values in sheet
    #sheet_data = [[sheet.cell_value(r, col)
                    # for col in range(sheet.ncols)]
                        #for r in range(sheet.nrows)]
                            
    coast = sheet.col_values(1, start_rowx=1, end_rowx=7297) #or end_rox=None for all values
    
    maxval = max(coast)
    minval = min(coast)
    
    maxpos = coast.index(maxval)+1
    minpos = coast.index(minval)+1
    
    maxtime = sheet.cell_value(maxpos,0)
    realmaxtime = xlrd.xldate_as_tuple(maxtime,0)
    mintime = sheet.cell_value(minpos,0)
    realmintime = xlrd.xldate_as_tuple(mintime,0)
    
    avgcoast = float(sum(coast))/ len(coast)
    
    data = {
            'maxtime': realmaxtime,
            'maxvalue': maxval,
            'mintime': realmintime,
            'minvalue': minval, 
            'avgcoast': avgcoast
    }
    return data    
    
http://www.w3schools.com/json/
http://www.json.org/

### Lesson 1.15
# To experiment with this code freely you will have to run this code locally.
# Take a look at the main() function for an example of how to use the code.
# We have provided example json output in the other code editor tabs for you to
# look at, but you will not be able to run any queries through our UI.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

# query parameters are given to the requests.get function as a dictionary; this
# variable contains some starter parameters.
query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    # This is the main function for making queries to the musicbrainz API.
    # A json document should be returned by the query.
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    # This adds an artist name to the query parameters before making
    # an API call to the function above.
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    # After we get our output, we can format it to be more readable
    # by using this function.
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
   
    results = query_by_name(ARTIST_URL, query_type["simple"], "The Beatles")
    pretty_print(results)

    artist_id = results["artists"][0]["id"]
    print "\nARTIST:"
    pretty_print(results["artists"][0])

    artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    releases = artist_data["releases"]
    print "\nONE RELEASE:"
    pretty_print(releases[0], indent=2)
    release_titles = [r["title"] for r in releases]

    print "\nALL TITLES:"
    for t in release_titles:
        print t == "Beatles"

### Problem Set 1.1 

df = '/Users/bindupaul/Desktop/745090.csv'
def parse_file (df):
    data = []
    with open(df, "rb") as f: 
        header = f.readline().split(',')
        name = header[1].strip('"')
        reader = csv.reader(f)
        line = [row for row in reader]
        data = line[1:]
    return (name, data)
    
### Problem Set 1.2 
import xlrd
import os
import csv
from zipfile import ZipFile   

df = "2013_ERCOT_Hourly_Load_Data.xls" 

#def open_zip(df):
#    with ZipFile('{0}.zip'.format(df), 'r') as myzip:
#        myzip.extractall()

def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = {}
    # process all rows that contain station data
    for n in range (1, 9):
        station = sheet.cell_value(0, n)
        cv = sheet.col_values(n, start_rowx=1, end_rowx=None)

        maxval = max(cv)
        maxpos = cv.index(maxval) + 1
        maxtime = sheet.cell_value(maxpos, 0)
        realtime = xlrd.xldate_as_tuple(maxtime, 0)
        data[station] = {"maxval": maxval,
                         "maxtime": realtime}
    return data

def save_file(data, filename):
    with open(filename, "w") as f:
        w = csv.writer(f, delimiter='|')
        w.writerow(["Station", "Year", "Month", "Day", "Hour", "Max Load"])
        for s in data:
            #picking the values from 'maxtime' and use underscore to omit values
            year, month, day, hour, _ , _= data[s]["maxtime"]
            w.writerow([s, year, month, day, hour, data[s]["maxval"]])

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This exercise shows some important concepts that you should be aware about:
- using codecs module to write unicode files
- using authentication with web APIs
- using offset when accessing web APIs

To run this code locally you have to register at the NYTimes developer site 
and get your own API key. You will be able to complete this exercise in our UI without doing so,
as we have provided a sample result.

Your task is to process the saved file that represents the most popular (by view count)
articles in the last day, and return the following data:
- list of dictionaries, where the dictionary key is "section" and value is "title"
- list of URLs for all media entries with "format": "Standard Thumbnail"

All your changes should be in the article_overview function.
The rest of functions are provided for your convenience, if you want to access the API by yourself.
"""
import json
import codecs
import requests

URL_MAIN = "http://api.nytimes.com/svc/"
URL_POPULAR = URL_MAIN + "mostpopular/v2/"
API_KEY = { "popular": "",
            "article": ""}


def get_from_file(kind, period):
    filename = "popular-{0}-{1}.json".format(kind, period)
    with open(filename, "r") as f:
        return json.loads(f.read())


def article_overview(kind, period):
    data = get_from_file(kind, period)
    titles = []
    urls = []
    for i in data:
        titles.append({i["section"]:i["title"]})
        for m in i["media"]: 
            for mm in m["media-metadata"]:
                if mm["format"] == "Standard Thumbnail":
                    urls.append(mm["url"])
            
    return (titles, urls)


def query_site(url, target, offset):
    # This will set up the query with the API key and offset
    # Web services often use offset paramter to return data in small chunks
    # NYTimes returns 20 articles per request, if you want the next 20
    # You have to provide the offset parameter
    if API_KEY["popular"] == "" or API_KEY["article"] == "":
        print "You need to register for NYTimes Developer account to run this program."
        print "See Intructor notes for information"
        return False
    params = {"api-key": API_KEY[target], "offset": offset}
    r = requests.get(url, params = params)

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def get_popular(url, kind, days, section="all-sections", offset=0):
    # This function will construct the query according to the requirements of the site
    # and return the data, or print an error message if called incorrectly
    if days not in [1,7,30]:
        print "Time period can be 1,7, 30 days only"
        return False
    if kind not in ["viewed", "shared", "emailed"]:
        print "kind can be only one of viewed/shared/emailed"
        return False

    url += "most{0}/{1}/{2}.json".format(kind, section, days)
    data = query_site(url, "popular", offset)

    return data


def save_file(kind, period):
    # This will process all results, by calling the API repeatedly with supplied offset value,
    # combine the data and then write all results in a file.
    data = get_popular(URL_POPULAR, "viewed", 1)
    num_results = data["num_results"]
    full_data = []
    with codecs.open("popular-{0}-{1}.json".format(kind, period), encoding='utf-8', mode='w') as v:
        for offset in range(0, num_results, 20):        
            data = get_popular(URL_POPULAR, kind, period, offset=offset)
            full_data += data["results"]
        
        v.write(json.dumps(full_data, indent=2))




























                        
    