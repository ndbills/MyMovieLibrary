from project import db
import User,Movie

class Collection(db.Document):
    user = db.ReferenceField(User.User)
    movies = db.ListField(db.ReferenceField(Movie.Movie))

    def addMovie(self,movie):
    	self.movies.append(movie)
        return self