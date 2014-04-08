import User

class Collection(db.Document):
    user = db.ReferenceField(User)
    movies = db.ListField(db.DocumentField('Movie'))