import pymongo

# Connect to the database
myclient = pymongo.MongoClient("210.45.76.110",27017)
# connection = pymongo.MongoClient("mongodb://localhost")
db=myclient["socomp"]
db.authenticate("socomp","linke-2022")
collection=db["votes"] # collection db["votes"]/db["cosponsors"]/db["members"]
rets=collection.find({"vote":"N"})
print(rets.count())

# dblist=myclient.list_database_names()
# print(dblist)
