from project import db

class Group(db.Document):
	category = db.StringField(max_length=50, required=True)
	tags = db.ListField(db.StringField(max_length=50))