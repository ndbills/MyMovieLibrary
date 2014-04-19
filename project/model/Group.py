from project import db

class Group(db.Document):
	category = db.StringField(max_length=50, required=True)
	tags = db.ListField(db.StringField(max_length=50))

	def addTag(self,tag):
		if tag not in self.tags:
			self.tags.append(tag)
		return self

	def removeTag(self,tag):
		if tag in self.tags:
			self.tags.remove(tag)
		return self    

	def __str__(self):
		return "Category: %s - %s" % (self.category, self.tags)

	def __repr__(self):
		return "{%s}" % (self.category)