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


    # if prod_env == ProductionEnvironment.PRODUCTION:
    #     host = os.getenv("PROD1_MONGO_HOST")
    #     database = os.getenv("PROD1_MONGO_DATABASE")
    #     un = os.getenv("PROD1_MONGO_USERNAME")
    #     pw = os.getenv("PROD1_MONGO_PASSWORD")
    # elif prod_env == ProductionEnvironment.PRODUCTION2:
    #     host = os.getenv("PROD2_MONGO_HOST")
    #     database = os.getenv("PROD2_MONGO_DATABASE")
    #     un = os.getenv("PROD2_MONGO_USERNAME")
    #     pw = os.getenv("PROD2_MONGO_PASSWORD")
    # elif prod_env == ProductionEnvironment.GEO_ONLY:
    #     host = os.getenv("GEO_ONLY_MONGO_HOST")
    #     database = os.getenv("GEO_ONLY_MONGO_DATABASE")
    #     un = os.getenv("GEO_ONLY_MONGO_USERNAME")
    #     pw = os.getenv("GEO_ONLY_MONGO_PASSWORD")
    # elif prod_env == ProductionEnvironment.QA:
    #     host = os.getenv("QA_MONGO_HOST")
    #     database = os.getenv("QA_MONGO_DATABASE")
    #     un = os.getenv("QA_MONGO_USERNAME")
    #     pw = os.getenv("QA_MONGO_PASSWORD")
    # elif prod_env == ProductionEnvironment.CENSUS_DATA1:
    #     host = os.getenv("CENSUS_DATA1_HOST")
    #     database = os.getenv("CENSUS_DATA1_DATABASE")
    #     un = os.getenv("CENSUS_DATA1_USERNAME")
    #     pw = os.getenv("CENSUS_DATA1_PASSWORD")
    # elif prod_env == ProductionEnvironment.CENSUS_DATA2:
    #     host = os.getenv("CENSUS_DATA2_HOST")
    #     database = os.getenv("CENSUS_DATA2_DATABASE")
    #     un = os.getenv("CENSUS_DATA2_USERNAME")
    #     pw = os.getenv("CENSUS_DATA2_PASSWORD")
    # elif prod_env == ProductionEnvironment.MARKET_TRENDS:
    #     host = os.getenv("MARKET_TRENDS_MONGO_HOST")
    #     database = os.getenv("MARKET_TRENDS_MONGO_DATABASE")
    #     un = os.getenv("MARKET_TRENDS_MONGO_USERNAME")
    #     pw = os.getenv("MARKET_TRENDS_MONGO_PASSWORD")
    # elif prod_env == ProductionEnvironment.MARKET_MAPS:
    #     host = os.getenv("MARKET_MAPS_HOST")
    #     database = os.getenv("MARKET_MAPS_DATABASE")
    #     un = os.getenv("MARKET_MAPS_USERNAME")
    #     pw = os.getenv("MARKET_MAPS_PASSWORD")
    #
    # connection_string = 'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority' \
    #     .format(un, pw, host, database)
    #
    #
    # client = MongoClient(connection_string)
    #
    # return client

