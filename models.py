#import pymongo
#from pymongo import MongoClient
from mongoengine import connect, Document, ListField, StringField, URLField, DictField


connect(db="lmsbot", host="localhost", port=27017)
#client = MongoClient()
#database = client.lmsbot
#events = database.events


class Events(Document):
    title = StringField(required=True, max_length=200)
    date = StringField(required=True, max_length=200)
    #contributors = ListField(StringField(max_length=20))
    #url = URLField(required=True)

class Course(Document):
    code = StringField(required=True, max_length=50)
    title = StringField(required=True, max_length=100)
    portal_id = StringField(required=True, max_length=100)
    facilitator = StringField(required=False, max_length=200)
    zoom_link = URLField(required=False)
    recent_activities = ListField(DictField())
    upcoming_events = ListField(DictField())
    latest_announcements = ListField(DictField())




#e = Events(title="Test-3", date="Wdnesday, 30th, 2021")
#e.save()
#a = [{'title': 'Quiz  I - Monosaccharides closes', 'date': 'Tomorrow'}, {'title': 'Quiz - Testing Foundational Concepts closes', 'date': 'Friday, 26 March'}]
#c = Course(
#    code="ABN 200", 
#    title="Introduction to Agricultural Biochemistry", 
#    portal_id="141", 
#    facilitator="Dr. Oluwafunmilayo O. Adeleye",
#    recent_activities=a
#    )
#c.save()
#print(Course.objects())