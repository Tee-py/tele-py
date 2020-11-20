import json
import uuid

class DataBase:

    def __init__(self, file_name):
        self._file_name = file_name

    def object_already_exist(self, object, collection_name):
        data = self.load()
        #print(object["id"])
        collection = list(filter(lambda obj:list(obj.keys())[0]==collection_name, data))[0]
        data_exist = list(filter(lambda obj:obj["id"]==object["id"], collection[collection_name]))
        if data_exist:
            position = collection[collection_name].index(data_exist[0])
            collection[collection_name][position] = object
            #print("Data Exists")
            return True, collection
        collection[collection_name].append(object)
        #print("Doesn't Exist")
        return False, collection



    def save_object(self, collection_name, data):
        if not self.collection_exist(collection_name):
            self.create_collection(collection_name)
        exists, collection = self.object_already_exist(data, collection_name)
        dat = self.load()
        saved_collection = list(filter(lambda obj:list(obj.keys())[0]==collection_name, dat))[0]
        position = dat.index(saved_collection)
        #collection[collection_name].append(data)
        dat[position] = collection
        self.dump(dat)
        return True

    def retrieve_object(cls, model_name, id):
        pass
    
    def collection_exist(self, name):
        data = self.load()
        def filter_func(obj, name):
            try:
                obj[name]
                return True
            except:
                return False
        collection_filter = filter(lambda obj:filter_func(obj, name),data)
        #print(collection_filter)
        if len(list(collection_filter)) == 0:
            return False
        return True

    def create_collection(self, collection_name):
        try:
            if self.collection_exist(collection_name):
                return True, f"Collection: {collection_name} Already Exist in the Database"
            data = self.load()
            data.append({collection_name: []})
            self.dump(data)
            return True
        except:
            return False

    def delete_collection(self, collection_name):
        if not self.collection_exist(collection_name):
            return f"Collection: {collection_name} does not Exist In the Database"
        new_data = filter(lambda obj:list(obj.keys())[0] != collection_name, self.load())
        self.dump(list(new_data))
        return f"Collection: {collection_name} deleted from DataBase Successfully"

    def flush(self):
        self.dump([])
        return True

    def load(self):
        with open(self._file_name) as db:
            data = json.load(db)
            return data

    def dump(self, data):
        with open(self._file_name, "w") as db:
            json.dump(data, db, indent=4)
            return True


class User:

    def __init__(self, name, chat_id):
        self.id = uuid.uuid4()
        self.chat_id = chat_id
        self.name = name

    def save(self):
        try:
            DataBase.save_object(model_name="User", data={
                "id": self.id, 
                "chat_id": self.chat_id,
                "name": self.name}
            )
            return True
        except:
            return False

    @classmethod
    def retrieve(cls, id):
        try:
            return DataBase.retrieve_object(model_name="User", id=id)
        except:
            return False

    def delete(self):
        try:
            DataBase.delete_object(model_name="User", id=self.id)
            return True
        except:
            return False