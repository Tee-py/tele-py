from db import DataBase, User
import time

db = DataBase("db.json")

#Loading Function Test Passsed
#print(db.load())

#Flushing Database Passed
#time.sleep(2)
#print(db.flush())

#Test for Deleting Collections Passed
#print("\nsleeping for 5 seconds ...\n")
#time.sleep(5)
#print(db.delete_collection("Hi"))
#for col in col_lst:
#    print(db.delete_collection(col))

#Create_collection and collection_exist Function Passed
col_lst = ["User", "Images", "Students", "Teachers", "Country", "States", "News"]
for col in col_lst:
    print(db.create_collection(col))

#Testing Saving Objects
print(db.save_object("Saviours", {"id": "Hello"}))
print(db.save_object("Saviours", {"id": "Hello", "status": "Wealthy"}))
print(db.save_object("Saviours", {"id": "Hel", "status": "Wealthy"}))
print(db.save_object("User", {"id":"162tebwejknevhk", "chat_id": "31456789", "name": "Emmanuel"}))
print(db.save_object("User", {"id":"162tebwejknevhk", "chat_id": "31456789", "name": "Teepy"}))
print(db.save_object("User", {"id":"162tebwejevhk", "chat_id": "31456789", "name": "Teepy"}))