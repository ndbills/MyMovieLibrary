#!/usr/bin/python
import sys, logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/MyMovieLibrary/')

from project import app as application