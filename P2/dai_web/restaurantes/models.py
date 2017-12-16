import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://rafa:daipass123@cluster0-shard-00-00-1ivyw.mongodb.net:27017,cluster0-shard-00-01-1ivyw.mongodb.net:27017,cluster0-shard-00-02-1ivyw.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = client.test
restaurantes = db.restaurants

def find_restaurant(key, value):
    return restaurantes.find( {key: value})

def find_restaurant(key, value, page=0, lim=12):
    return restaurantes.find( {key: value}).skip( page * lim ).limit( lim )
