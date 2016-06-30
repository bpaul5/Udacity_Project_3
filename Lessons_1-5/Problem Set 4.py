### Lesson 4 

from pymongo import MongoClient

db.datas.find().count() or findOne() #finds the first value
db.datas.insert(data)
db.datas.remove() #removes data one by one 
db.datas.drop() #removes all data and metadata 

# I only want to see 'name' and no id since id will print by default
projection = {"_id" : 0, "name" : 1}

#Inequality operators 
$gt (greater than)
$lt
$gte (greater than or equal to)
$lte
$ne (not equal to)
query = {"population" : {"$gt" : 250, "$lte" : 500}}

#all city names that start with 'X'
query = {"name" : {"$gte" : "X", "$lt" : "Y"}}

#all city that have a specific date 
query = {"foundingDate" : {"$gt" : datetime(1837, 1, 1), 
                           "$lte" : datetime(1837, 12, 31)}}
#does governmentType exist = 1 or no = 0
db.cities.find({"governmentType" : {"$exists" : 1}}).count().pretty()

#regular expression queries google PCRE for more info
#finds motto that have friendship/Friendship or pride 
db.cities.find({"motto" : {"$regex": "[Ff]riendship|[Pp]ride"}})

#specify an array of values NOT ALL VALUES HAVE TO BE PRESENT
db.autos.find({"modelYears" : {"$in" : [1965, 1966, 1967]}}).count()

#specify an array of values that HAVE TO BE PRESENT 
db.autos.find({"modelYears" : {"$all" : [1965, 1966]}}).count()

#multiple queries 
query = {"manufacturer" : "Ford Motor Company", 
"assembly" : {"$in" : ["Germany", "Japan", "United Kingdom"]}}

#use dot (.) to query sub arrays of arrays
entities.hastag.tweet

#to modify existing document 
db.datas.save(data)

#$set will add or change the isoCountryCode 
db.cities.update({"country" : "Germany"}, 
                 {"$set" : {
                     "isoCountryCode" : "DUE"
                }})
#$unset will delete the isoCountryCode 
                {"$unset" : {
                    "isoCountryCode" : ""
                }}
                
def trim_parenthesis(v):
    pos = v.find('(')
    if pos > -1:
        return v[:pos-1]
    else:
        return v 

def remove_key(d):
    r = dict(d)
    for key in d:
        if key not in FIELDS:
            del r[key]
    return r
    

        




































