Movie Collection
================

This project aims to solve the problem that many a movie collector faces with a growing library of movies. With the expansion of information available on the web today, we want to build an application that will help movie collectors (or those with movies) keep track of their movies in a flexible, convenient way. This project will not only aim to help record the movies but allow for responsible borrowing and lending of movies and help users to find the right movie in their collection to meet their mood.

The idea is to create a responsive front-end that consumes a RESTful web service that we will create. Users will be able to create a profile, add their movies (or select movies if they already exist in the DB), and create collections (favorites, etc.).

#Features of this project include:

* User Login
* Add/Delete/Modify Movies
* Organize Movies (into different lists)
* Sort/Search movies
* Lend/Borrow Movies
* Send email reminders to get movies back 
* Support gmail, outlook.com, yahoo mail

#Framework

* Backend: Flask
* Frontend: BackboneJS + LoDashJS
* Storage: MongoDB

#Stretch Goals

* Social Integration (recommend movies, that kind of thing)
* Tag Movies (for sorting on different attributes)
* Rate Movies (0-5 star scale)
* Public lists (allow your whole neighborhood to see and request to borrow your movies)
* Movie Reviews for a movie
* Google Analytics

#Dependencies

*MongoDB
*https://github.com/wagnerrp/pytmdb3/

#Setup

Clone this directory
in the same parent folder you cloned this directory clone the following dependency https://github.com/wagnerrp/pytmdb3/
run the command `pip install -r requirements.txt`
update the `__init__.py` in the project folder to point to your mongodb server
start your mongodb server if it isn't running already
run the `python runserver.py` in the MyMovieLibrary directory
the application should be running on localhost:8080