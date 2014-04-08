from project import db

class Role(db.EmbeddedDocument):
    name = db.StringField(verbose_name="Comment", required=True)