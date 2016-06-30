### Lesson 5

https://docs.mongodb.org/manual/reference/operator/aggregation/

db.tweets.aggregate([   #group by source and display id
            {"$group" : {"id" : "$source",
                         "count" : {"$sum" : 1}}},
            {"$sort" : {"count" : -1}}])#descending order 
            
            #find following and followers greater than 0 
            [({"$match" : {"user.friends_count" : {"$gt" : 0},
                         "user.followers_count" : {"$gt" : 0}}},
            #include fields from the original doc, insert computed fields,
            #rename fields, create fields that hold subdocuments
            {"$project" : {"ratio" : { "$divide" : ["$user.followers_count",
                                                    "$user.friends_count"]},
                           "screen_name" : "$user.screen_name"}}, 
            {"$sort" : {"ratio" : -1}},
            {"$limit" : 1}])
            
pipeline = [{'$match': {'user.statuses_count': {'$gte': 100},
                            'user.time_zone': 'Brasilia'}},
                
                {'$project': {'screen_name': '$user.screen_name',
                              'followers': '$user.followers_count',
                              'tweets': '$user.statuses_count'}},
                
                {'$sort': {'followers': -1}}]
                
# $unwind an array and iterate over the values 
# size = 3 gives doc where len() is 3 
pipeline [,{'$unwind': '$entities.user_mentions'},
           {'$group': {'_id': '$user.screen_name',
                       'count': {'$sum': 1}}},
           {'$sort': {'count': -1}},
           {'$limit': 1}]

# group operators 
$sum 
$first # selects the first doc in group
$last 
$max 
$min
$avg
#{'$group': {'_id': '$isPartOf',
 #                           'regional_avg': {'$avg': '$population'}}}    
$addToSet # add value to array only once 
$push # similar to addToSet, instead it aggregates all values into an array
                
pipeline = [{'$match': {'country': 'India'}},
            {'$unwind': '$isPartOf'},
            {'$group': {'_id': '$isPartOf',
                        'regional_avg': {'$avg': '$population'}}},
            {'$group': {'_id': '$regional_avg',
                        'avg': {'$avg': '$regional_avg'}}}]

# indexing and geospatial indexing 

pipeline = [{"$match": {"country": "India"}},
                {"$unwind": "$isPartOf"},
                {"$group": {"_id": "$isPartOf",
                           "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 3}]
                
 pipeline = [{'$match': {'country': 'India'}},
                {'$unwind': '$isPartOf'},
                {'$group': {'_id': '$isPartOf',
                            'regional_avg': {'$avg': '$population'}}},
                {'$group': {'_id': 'regional_avg',
                            'avg': {'$avg': '$regional_avg'}}}]


































            