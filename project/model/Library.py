from project import db
import User, sys

class Library(db.Document):
	user = db.ReferenceField(User.User)
	unit = db.StringField(max_length=50) #what Document the Library's collection relates to 
	name = db.StringField(max_length=100, unique_with=['user','unit']) #name of the Library
	lookup_attribute = db.StringField(default='_id')
	collection = db.ListField(db.StringField())
	summary = db.StringField()

	def addUnit(self,unit):
		if self.unit == type(unit).__name__:
			value = unit[self.lookup_attribute]
			if value is not None and value not in self.collection:
				self.collection.append("%s" % value)
			else:
				return self	
		else:
			raise Exception("Cannot add %s to Library of %s" % (type(unit).__name__,self.unit))    		
		return self

	# @param index --represents the index in the Library collection of the object
	def hydrateUnit(self, index):
		if index < 0 or index > self.collection.count:
			raise Exception("Invalid index for Library %s" % self.name)
		attr = {}
		attr[self.lookup_attribute] = self.collection[index]
		model =  getattr(sys.modules["project.models.%s"%self.unit], self.unit)
		return model(**model._get_collection().find_one(**attr))

	def hydrateList(self):
		hydratedCollection = []
		model =  getattr(sys.modules["project.models.%s"%self.unit], self.unit)
		attr = {}
		for index, hash_value in self.collection:
			attr[self.lookup_attribute] = self.collection[index]
			hydratedCollection.append(model(**model._get_collection().find_one(**attr)))
		return hydratedCollection	