from project import db
import User, sys, copy, Group

class Library(db.Document):
	user = db.ReferenceField(User.User)
	unit = db.StringField(max_length=50) #what Document the Library's collection relates to 
	name = db.StringField(max_length=100, unique_with=['user','unit']) #name of the Library
	lookup_attribute = db.StringField(default='id')
	collection = db.ListField(db.StringField())
	
	def addUnit(self,unit):
		if self.unit == type(unit).__name__:
			value = str(unit[self.lookup_attribute])
			if value is not None and value not in self.collection:
				self.collection.append(value)
				self.save()
			else:
				return self	
		else:
			raise Exception("Cannot add %s to Library of %s" % (type(unit).__name__,self.unit))    		
		return self

	def removeUnit(self,unit):
		if self.unit == type(unit).__name__:
			value = str(unit[self.lookup_attribute])
			if value is not None and value in self.collection:
				self.collection.remove(value)
				self.save()
			else:
				return self	
		else:
			raise Exception("Cannot remove %s from Library of %s" % (type(unit).__name__,self.unit))    		
		return self

	# @param index --represents the index in the Library collection of the object
	def hydrateUnit(self, index):
		if index < 0 or index > self.collection.count:
			return None
		attr = {}
		attr[self.lookup_attribute] = self.collection[index]
		model =  getattr(sys.modules["project.model.%s" % self.unit], self.unit)
		return model.objects(**attr).first()

	def hydrateList(self):
		hydratedCollection = []
		model = getattr(sys.modules["project.model.%s" % self.unit], self.unit)
		for index, hash_value in enumerate(self.collection):
			attr = {}
			attr[self.lookup_attribute] = self.collection[index]
			unit = model.objects(**attr).first()
			hydratedCollection.append(unit)
		return hydratedCollection

	def searchCollection(self,keyword,exclude =[] ,heirarchy = []):
		"""
		Searches the collection of this library for matches to the keyword

		keyword   String: keyword to search for
		exclude   List: list of attributes to exclude from the search
		heirarchy List: order that matches should be returned 
		(first matches returned are always matches of multiple categories)

		Return List of unique matches ordered by heirarchy if provided else by attribute order of object
		"""
		import datetime
		hydratedCollection = self.hydrateList()
		model =  getattr(sys.modules["project.model.%s"%self.unit], self.unit)
		model_attributes = model.__dict__['_db_field_map'].keys()
		model_attributes = self.diff(model_attributes,exclude)
		if len(heirarchy) > 0:
			model_attributes = self.ordered_union(heirarchy,model_attributes)
		
		result = [[]]
		for attr in model_attributes:
			result.append([]);
		for unit in hydratedCollection:
			for index,attr in enumerate(model_attributes):
				value = unit[attr]
				if isinstance(value, datetime.datetime):
					value = value.isoformat()
				if isinstance(value,list) and keyword.lower() in (val.lower() for val in value): 
					result[index].append(unit)
				elif isinstance(value,basestring) and keyword.lower() in value.lower():
					result[index].append(unit)
				groups = Group.Group.objects(tags=keyword)
				for group in groups:
					if self.similar(group.tags,value):
						result[-1].append(unit)
						break

		finish_result = []
		for index,r in enumerate(result[:-1]):
			for val in r:
				for s in result[index:]:
					if val in s:
						if val not in finish_result:
							finish_result.append(val)
		
		for r in result:
			additions = self.diff(r,finish_result)
			finish_result.extend(additions)

		return finish_result	

	@staticmethod
	def diff(a, b):
		b = set(b)
		return [aa for aa in a if aa not in b]

	@staticmethod
	def ordered_intersect(a, b):
		b = set(b)
		return [aa for aa in a if aa in b]

	@staticmethod
	def ordered_union(a, b):
		a.extend(Library.diff(b,a))
		return a

	@staticmethod
	def similar(a,b):
		for val in a:
			if val in b:
				return True
		return False

	def __str__(self):
		return "Library {%s-%s}" % (self.name, self.unit)

	def __repr__(self):
		return self.__str__()
