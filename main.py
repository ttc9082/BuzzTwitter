import cgi
import datetime
import jinja2
import os
import urllib
import json
import webapp2

from client import *
from data_store import *

from google.appengine.ext import db
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class twitter(db.Model):
    results = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

def twitter_key(twitter_name=None):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return db.Key.from_path('twitter', twitter_name or 'default')

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        category = self.request.get('category')
        address = self.request.get('location').replace(" ", "+")
        NUMBER_PER_PAGE = '5'

        clause = category + address
        # twitest = sync_twits(category, address, NUMBER_PER_PAGE)
        if has_key(clause):
            twitest = retrieve_data(clause)
        else:
            twitest = sync_twits(category, address, NUMBER_PER_PAGE)
            store_data(clause, twitest)

        template_values = {
                            'twitest': twitest,
                            }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
