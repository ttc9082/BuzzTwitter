import cgi
import datetime
import jinja2
import os
import urllib
import json
import webapp2

from client import *
from data_store import *
from buzz_generator import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        category = self.request.get('category')
        address = self.request.get('location').replace(" ", "+")

        NUMBER_PER_PAGE = '5'
        NUMBER_OF_BUZZ = 2

        # twitest = sync_twits(category, address, NUMBER_PER_PAGE)
        if has_key(address, category):
            jsonstr = retrieve_data(address, category)
        else:
            jsonstr = sync_twits(category, address, NUMBER_PER_PAGE)
            store_data(address, category, jsonstr)

        twi_json = json.loads(jsonstr)
        twitest = twi_json['results']


        
        buzz_words = generate_buzz(twitest, NUMBER_OF_BUZZ)







        
        template_values = {
                            'twitest': twitest,
                            }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
