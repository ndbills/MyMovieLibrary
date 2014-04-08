class Group(db.Document):
	category = db.StringField(max_length=50, required=true)
    tags = db.ListField(db.EmbeddedDobumentField('Tag'))