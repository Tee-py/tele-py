from db import DataBase, User
import time

db = DataBase("db.json")

#Loading Function Test Passsed
print(db.load())

#Create_collection and collection_exist Function Passed
col_lst = ["User", "Images", "Students", "Teachers", "Country", "States", "News"]
for col in col_lst:
    print(db.create_collection(col))

#Test for Deleting Collections Passed
print("\nsleeping for 5 seconds ...\n")
time.sleep(5)
print(db.delete_collection("Hi"))
for col in col_lst:
    print(db.delete_collection(col))