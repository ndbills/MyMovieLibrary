from project import db
import datetime, Role

class User(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now(), required=True)
    email = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
    roles = db.ListField(db.StringField(max_length=50))

    def hasRole(self,role):
        return role in self.roles

    def addRole(self,role):
        self.roles.append(role)
        return self

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'email'],
        'ordering': ['-created_at']
    }