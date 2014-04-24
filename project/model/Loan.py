from project import db
import datetime
from User import User
from Movie import Movie

class Loan(db.Document):
	user = db.ReferenceField(User)
	movie = db.ReferenceField(Movie, unique_with=['user'])
	lent_date = db.DateTimeField(default=datetime.datetime.now, required=True)
	expected_return_date = db.DateTimeField(default=datetime.datetime.now, required=True)
	borrower_email = db.StringField()

	@staticmethod
	def create(user,movie,email,expected_return_date=None):
		info = Loan(user=user,movie=movie,borrower_email=email)
		if expected_return_date:
			info.expected_return_date = expected_return_date
		else:
			info.expected_return_date = info.expected_return_date + datetime.timedelta(days=7)
		info.save()
		return info


	def __str__(self):
		return "%s due %s" % (self.movie.title, self.expected_return_date.isoformat())

	def __repr__(self):
		return self.__str__()