class Movie(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    summary = db.StringField(max_length=10000, required=True)
    tags = db.ListField(db.EmbeddedDocumentField('Tag'))    
