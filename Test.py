import pandas as pd
import sys
import pymongo 
from pymongo import MongoClient

# sys.path.insert(0, "/home/minhthong/Documents")
import ConvertFile as cf

server = '127.0.0.1:27017'
dbname = 'Excel_Mongo'
collect_name_nlu = 'Nlu'
collect_name_story = "Story"

dataNlu = pd.read_excel("nlu.xlsx")
dataStory = pd.read_excel("story_copy.xlsx")


cf.excel2Mongo(dataNlu, server, dbname, collect_name_nlu, yml_name = "nlu")
cf.excel2Mongo(dataStory, server, dbname, collect_name_story, yml_name ="story")

cf.mongo2Yml(server, dbname, collect_name_nlu, yml_name ="nlu")
cf.mongo2Yml(server, dbname, collect_name_story, yml_name ="story")