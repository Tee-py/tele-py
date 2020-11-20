from db import DataBase, User

db = DataBase("db.json")

#Loading Function Test Passsed
print(db.load())

#Create_collection and collection_exist Function Passed
print(db.create_collection("User"))

