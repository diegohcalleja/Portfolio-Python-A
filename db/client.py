from pymongo import MongoClient
from db.secret_const.secret_const import MONGODB

##################################
###         BD en LOCAL        ###
##################################
    
##db_client = MongoClient().local

##################################
###         BD en ATLAS        ###
##################################

db_client = MongoClient(MONGODB).P2