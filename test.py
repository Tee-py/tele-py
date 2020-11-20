from db import DataBase, User

db = DataBase("db.json")

#print(db._file_name)
print(db.load())