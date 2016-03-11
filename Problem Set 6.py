# Lesson 6 

import xml.etree.cElementTree as ET
import re
from collections import defaultdict
import codecs
import json
import pymongo
from pymongo import MongoClient

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

filename = '/Users/bindupaul/Downloads/lincoln_nebraska.osm'

# display name of unique tags and amount of each
def count_tags(filename):
        tags = {}
        for event, elem in ET.iterparse(filename, events = ('start', 'end')):
            if elem.tag in tags and event == 'start':
                tags[elem.tag] += 1
            elif event == 'start':
                tags[elem.tag] = 1
            if event == 'end':
                elem.clear()
        return tags  

# used in the process_map()
# sorts the tags by specific characters and places them into dict 
def key_type(element, keys):
    if element.tag == "tag":
        k = element.get("k")
        if re.search(lower, k):
            keys['lower'] += 1
        elif re.search(lower_colon, k):
            keys['lower_colon'] += 1
        elif re.search(problemchars, k):
            keys['problemchars'] += 1
        else: 
            keys['other'] += 1
    return keys

# parse file and place tages into appropriate keys
def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

    
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Circle", "Highway", "Way"]
    
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road",
            "Rd": "Road",
            "N": "North",
            "NW": "North West",
            "W": "West",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Ln": "Lane",
            }
    
# used in audit() 
# finds street name and groups it or addes it to set() in not in expected variable
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

# used in audit() 
# find address from attribute
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# used to print out dict of street types not in expected variable
def audit(filename):
    osm_file = open(filename, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types
    
# used in better_name()    
def update_name(name, mapping):

    x = street_type_re.search(name).group()
    name = name.replace(x, mapping[x])
    return name
    
# Prints corrected street names 
def better_name():
    st_types = audit(filename)
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name

# used in process_map2()            
# use to obtain attributes from tages and sort them into a dict also creates the proper layout of dict            
def shape_element(element):
    d = {}
    created = {"version": None, "changeset": None, "timestamp": None, "user": None, "uid": None}
    if element.tag == "node" or element.tag == "way" :
        for i in element.attrib.keys():
            if i in created.keys():
                created[i] = element.attrib[i]
                
            elif element.attrib[i] == element.get('lat') or element.attrib[i] == element.get('lon'):
                pos = []
                pos.append(float(element.get('lat')))
                pos.append(float(element.get('lon')))
                d['pos'] = pos
                
            else:
                d[i] = element.get(i)
                d['type'] = element.tag
                
        d['created'] = created
        
        address = {}
        node_refs = []
        for subtag in element: 
            if subtag.tag == 'tag': 
                if re.search(problemchars, subtag.get('k')):
                    pass
                
                elif re.search(r'\w+:\w+:\w+', subtag.get('k')):
                    pass
                
                elif subtag.get('k').startswith('addr:'):
                    address[subtag.get('k')[5:]] = subtag.get('v')
                    d['address'] = address
                    
                else:
                    d[subtag.get('k')] = subtag.get('v')
                    
            elif subtag.tag == 'nd':
                node_refs.append(subtag.attrib['ref'])
                
        if node_refs:
            d['node_refs'] = node_refs
        
        return d
    
    else:
        return None
        
# proces the file into JSON format for inserting into MongoDB                        
def process_map2(filename, pretty = False):
    file_out = "{0}.json".format(filename)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(filename):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data      

# Sample of the format of the data 
{
"id": "2406124091",
"type": "node"
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}       

# db_name = 'street'        
def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

# group by phone numbers     
def make_pipeline():
    pipeline = [{'$group': {'_id': '$phone',
                            'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 5}]
    return [doc for doc in db.street.aggregate(pipeline)]

# to fix phone numbers (1)
def find_numbers(results): 
    numbers = []
    for i in results:
        for k, v in i.iteritems():
            if v == None:
                continue 
            elif v.startswith('402'):
                continue
            else:
                numbers.append(v)
    return numbers 

def fix_numbers():
    data = []
    num = find_numbers(results)
    for i in num:
        new = i.replace("/", "-").replace(" ", "-").replace("1", "").replace("001", "")
        data.append(new)
    return data

# used to find the type of nodes (2)
def make_pipeline():     
pipeline = [{'$group': {'_id': '$type',                             
                 'count': {'$sum': 1}}},                 
       {'$sort': {'count': -1}}]     
return pipeline


# Used to group by cuisine (3)
def make_pipeline():            
    pipeline = [{'$group': {"_id": "$cuisine",
                               "count": {"$sum": 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 100}]
    return [doc for doc in db.street.aggregate(pipeline)]

# Used to group by the name of sandwich shops (4)
def make_pipeline():            
    pipeline = [{'$match': {"cuisine": "sandwich"}},
                {'$group': {'_id': '$name',
                            'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 100}]
    return [doc for doc in db.street.aggregate(pipeline)]

# Used to group by postal code (5)
def make_pipeline():            
    pipeline = [{'$group': {"_id": "$address.postcode",
                               "count": {"$sum": 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10}]
    return [doc for doc in db.street.aggregate(pipeline)]

# Used to find the grade level of schools (6)
def make_pipeline():
    pipeline = [{"$match": {"amenity": "school"}},
                {"$project": {"name": "$name"}},
                {"$limit" : 300}]
    return [doc for doc in db.street.aggregate(pipeline)]

x = make_pipeline 

 def get():
    elementary = 0
    middle = 0
    high = 0
    for i in x:
        for k,v in i.iteritems():
            v2 = str(v)
            if v2.startswith("5"):
                continue
            else:
                if v2.count("Middle") == 1 or v2.count("Junior") == 1:
                    middle += 1
                if v2.count("Elementary") == 1:
                    elementary += 1
                if v2.count("High") == 1:
                    high += 1
    print [elementary, middle, high]


                
                
                
                
                
                
                
                
                
                
                
                