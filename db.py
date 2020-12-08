import json
import uuid

class DataBase:

    def __init__(self, file_name):
        self._file_name = file_name

    def object_already_exist(self, object, collection_name):
        data = self.load()
        #print(object)
        collection = list(filter(lambda obj:list(obj.keys())[0]==collection_name, data))[0]
        print(object["id"])
        data_exist = list(filter(lambda obj:str(obj["id"])==object["id"], collection[collection_name]))
        #print(data_exist)
        if data_exist:
            position = collection[collection_name].index(data_exist[0])
            collection[collection_name][position] = object
            #print("Exists")
            return True, collection
        collection[collection_name].append(object)
        return False, collection

    def save_object(self, collection_name, data):
        #print(data)
        if not self.collection_exist(collection_name):
            self.create_collection(collection_name)
        exists, collection = self.object_already_exist(data, collection_name)
        dat = self.load()
        saved_collection = list(filter(lambda obj:list(obj.keys())[0]==collection_name, dat))[0]
        position = dat.index(saved_collection)
        dat[position] = collection
        self.dump(dat)
        return True

    def delete_object(self, collection_name, id):
        data = self.load()
        collection = list(filter(lambda obj:list(obj.keys())[0]==collection_name, data))[0]
        position = data.index(collection)
        #print(collection)
        #print(position)
        new_collection = list(filter(lambda obj:str(obj["id"])!=id, collection[collection_name]))
        #print(new_collection)
        data[position][collection_name] = new_collection
        self.dump(data)

    def retrieve_object(self, collection_name, id):
        if not self.collection_exist(collection_name):
            return f"Collection: {collection_name} does not Exist in the DataBase"
        data = self.load()
        collection = list(filter(lambda obj:list(obj.keys())[0]==collection_name, data))[0]
        object_filter = list(filter(lambda obj:obj["id"]==id, collection[collection_name]))
        if object_filter:
            return object_filter[0]
        else:
            return False
    
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

    def retrieve_collection(self, collection_name):
        if not self.collection_exist(collection_name):
            print(f"Collection: {collection_name} does not Exist In the Database")
            return False
        data = list(filter(lambda obj:list(obj.keys())[0] == collection_name, self.load()))[0]
        print(f"Collection: {collection_name} retrieved from DataBase Successfully")
        return data[collection_name]
        
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

    db = DataBase("db.json")
    def __init__(self, name, chat_id, id=None):
        if not id:
            self.id = uuid.uuid4()
        else:
            self.id = id
        self.chat_id = chat_id
        self.name = name

    def save(self):
        cls = User
        cls.db.save_object(collection_name="User", data={
            "id": str(self.id), 
            "chat_id": self.chat_id,
            "name": self.name}
        )
        return True
 
    def __str__(self):
        return f"User Object: {self.id}"

    @classmethod
    def retrieve(cls, id):
        data = cls.db.retrieve_object("User", id)
        return User(id=data["id"], chat_id=data["chat_id"],name=data["name"]) if data else f"User Object: {id} Does Not Exist in the DataBase"

    def delete(self):
        cls = User
        cls.db.delete_object(collection_name="User", id=self.id)
        return True
    
    @classmethod
    def chat_id_exists(cls, chat_id):
        data = cls.db.load()
        collection = list(filter(lambda obj:list(obj.keys())[0]=="User", data))[0] if list(filter(lambda obj:list(obj.keys())[0]=="User", data)) else []
        chat_id_filter = list(filter(lambda obj:obj["chat_id"]==chat_id, collection["User"])) if collection else []
        if chat_id_filter:
            return True
        return False


class BotUser(User):

    def __init__(self, name, chat_id, id=None, dls=None, max_loss=None):
        User.__init__(self, name, chat_id, id)
        self._dls = dls
        self._max_loss = max_loss

    def __str__(self):
        return f"BotUser Object: {self.name} {self.id}"

    def save(self):
        clss = BotUser
        clss.db.save_object(collection_name="User", data={
            "id": str(self.id), 
            "chat_id": self.chat_id,
            "name": self.name,
            "default_lot_size": self._dls,
            "max_loss_per_trade": self._max_loss
            }
        )
        return True
    @classmethod
    def retrieve(cls, chat_id):
        data = cls.retrieve_by_chat_id(chat_id)
        if data:
            return BotUser(
                id=data["id"], 
                chat_id=data["chat_id"],
                name=data["name"], 
                dls=data["default_lot_size"], 
                max_loss=data["max_loss_per_trade"]
            ) if data else f"User Object: {id} Does Not Exist in the DataBase"
        return False
   
    @classmethod
    def retrieve_by_chat_id(cls, chat_id):
        if not cls.db.collection_exist("User"):
            print(f"Collection: {collection_name} does not Exist in the DataBase")
            return False
        data = cls.db.load()
        collection = list(filter(lambda obj:list(obj.keys())[0]=="User", data))[0]
        object_filter = list(filter(lambda obj:obj["chat_id"]==chat_id, collection["User"]))
        if object_filter:
            return object_filter[0]
        else:
            return False
    
    def delete(self):
        user = BotUser.retrieve_by_chat_id(self.chat_id)
        BotUser.db.delete_object(collection_name="User", id=user["id"])