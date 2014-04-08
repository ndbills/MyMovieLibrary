import Role

class User(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    email = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
    roles = db.ListField(db.EmbeddedDocumentField('Role'))

    def hasRole(self,role):
        return role in roles

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'email'],
        'ordering': ['-created_at']
    }