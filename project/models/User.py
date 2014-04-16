from project import db
import datetime, hashlib, random

class User(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now(), required=True)
	email = db.StringField(max_length=255, required=True, unique=True)
	salt = db.StringField(max_length=255, required=True)
	password = db.StringField(max_length=255, required=True)
	roles = db.ListField(db.StringField(max_length=50))

	# def __init__(self, email, password):
	# 	super(User,self).__init__(email=email, password=password)
	# 	self.email = email
	# 	self.salt = str(random.getrandbits(128))
	# 	self.password = hashlib.sha224(self.salt.join(password)).hexdigest()

	def hasRole(self,role):
		return role in self.roles

	def addRole(self,role):
		self.roles.append(role)
		return self

	@staticmethod
	def validateUser(email, password):
		user = User.objects(email=email).first()
		if user == None:
			raise Exception('Invalid credentials supplied');
		password = hashlib.sha224(user.salt.join(password)).hexdigest()
		if user.password == password:
			return user
		else:
			raise Exception('Invalid credentials supplied');  

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'email'],
		'ordering': ['-created_at']
	}