from project import db
import datetime, hashlib, random

class User(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now(), required=True)
	email = db.StringField(max_length=255, required=True, unique=True)
	salt = db.StringField(max_length=255, required=True)
	password = db.StringField(max_length=255, required=True)
	roles = db.ListField(db.StringField(max_length=50))

	def hasRole(self,role):
		return role in self.roles

	def addRole(self,role):
		if role not in self.roles:
			self.roles.append(role)
		return self

	def removeRole(self,role):
		if role in self.roles:
			self.roles.remove(role)
		return self	

	def changePassword(self,password):
		self.password =	hashlib.sha224(self.salt.join(password)).hexdigest()
		self.save()
		return self

	@staticmethod
	def createUser(email, password):
		user = User(email=email)
		user.salt = str(random.getrandbits(128))
		user.password = hashlib.sha224(user.salt.join(password)).hexdigest()
		user.save()
		return user

	@staticmethod
	def validateUser(email, password):
		user = User.objects(email=email).first()
		if user == None:
			raise Exception('Invalid credentials supplied');
		password = hashlib.sha224(user.salt.join(password)).hexdigest()
		if user.password == password:
			return user
		else:
			return None

	def __str__(self):
		return self.email

	def __repr__(self):
		return {'created': self.created, 'email': self.email, 'roles': self.roles, 'id':str(self.id)}

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'email'],
		'ordering': ['-created_at']
	}