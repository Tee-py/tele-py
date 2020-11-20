from db import DataBase, User

db = DataBase("db.json")

#Loading Function Test Passsed
print(db.load())

#Create_collection and collection_exist Function Passed
col_lst = ["User", "Images", "Students", "Teachers", "Country", "States", "News"]
for col in col_lst:
    print(db.create_collection(col))