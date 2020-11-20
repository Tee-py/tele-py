from db import DataBase, User

db = DataBase("db.json")

#Loading Function Test Passsed
print(db.load())

#Create_collection Function Passed
print(db.create_collection("User"))