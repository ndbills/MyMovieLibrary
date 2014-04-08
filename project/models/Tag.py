class Tag(db.EmbeddedDocument):
	name = db.StringField(max_length=100, required=True)
    group_id = db.ReferenceField(Group) 