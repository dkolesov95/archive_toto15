from pymongo import MongoClient




# MONGOCLIENT = MongoClient()
# DATABASE = MONGOCLIENT['toto15']
# COLLECTION = DATABASE[TOTO15_SITE]



def write_info(toto_site, info):
        
    mongoclient = MongoClient()
    database = mongoclient['toto15']
    collection = database[toto_site]

    collection.insert_one(info)