import json
import uuid

class DataBase:

    def __init__(self, file_name):
        self._file_name = file_name

    @classmethod
    def save_object(cls, model_name, data):
        pass

    @classmethod
    def retrieve_object(cls, model_name, id):
        pass
    
    def create_collection(self, collection_name):
        try:
            data = self.load()
            data.append({collection_name: []})
            self.dump(data)
            return True
        except:
            return False

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