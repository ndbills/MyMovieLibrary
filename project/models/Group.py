import Tag

class Group(db.Document):
    category = db.StringField(max_length=50, required)
    tags = db.ListField(db.EmbeddedDobumentField('Tag'))