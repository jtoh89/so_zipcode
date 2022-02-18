import sys
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pandas import DataFrame
import pandas as pd
import json
from bson import json_util

def insert_list_mongo(list_data, dbname, collection_name, collection_update_existing=False):
    client = connect_to_client()
    db = client[dbname]
    collection = db[collection_name]

    try:
        if collection_update_existing or collection_update_existing == {}:
            collection.delete_many(collection_update_existing)

        collection.insert_many(list_data)
    except:
        print("!!! ERROR could not store insert_list_mongo to Mongo!!!")
        sys.exit()



def connect_to_client():
    load_dotenv()
    host = os.getenv("MARKET_MAPS_HOST")
    database = os.getenv("MARKET_MAPS_DATABASE")
    un = os.getenv("MARKET_MAPS_USERNAME")
    pw = os.getenv("MARKET_MAPS_PASSWORD")

    connection_string = 'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority' \
        .format(un, pw, host, database)

    client = MongoClient(connection_string)

    return client

