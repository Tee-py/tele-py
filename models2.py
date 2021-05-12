#import pymongo
#from pymongo import MongoClient
from mongoengine import connect, Document, ListField, StringField, URLField, DictField, DecimalField


connect(db="shitcoin-db", host="mongodb+srv://teepy:mongo-teepy2021@teepycluster.ircf4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


class Trader(Document):
    chat_id = StringField(required=True, max_length=100)
    name = StringField(required=True, max_length=100)
    portfolio = ListField(DictField())

class Token(Document):
    owner_id = StringField(required=True, max_length=100)
    name = StringField(required=True, max_length=200)
    contract_address = StringField(required=True, max_length=500)
    entry_price = DecimalField(required=True)