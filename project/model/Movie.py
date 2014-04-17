from project import db
import datetime

class Movie(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    summary = db.StringField(max_length=10000, required=True)
    tags = db.ListField(db.StringField(max_length=50))

    def addTag(self,tag):
        self.tags.append(tag)
        return self

    def __str__(self):
    	return self.title

    def __repr__(self):
    	return self.__str__()    