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
from analyst import *

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

        NUMBER_PER_PAGE = '100'
        NUMBER_OF_BUZZ = 10
        NUMBER_OF_TWITS_PER_BUZZ = 4

        # twitest = sync_twits(category, address, NUMBER_PER_PAGE)
        if has_key(address, category):
            jsonstr = []
            pages = retrieve_data(address, category)
            for i in range(len(pages)):
                jsonstr.append(json.loads(pages[i].results))
            # print jsonstr
        else:
            jsonstr = sync_twits(category, address, NUMBER_PER_PAGE)
            # print jsonstr
            for pages in jsonstr:
                store_data(address, category, pages)

        # twi_json = json.loads(jsonstr)
        # twitest = twi_json['results']
        twitest = jsonstr

        buzz_words = generate_buzz(twitest, NUMBER_OF_BUZZ)
        final_structs = generate_struct(twitest, buzz_words, NUMBER_OF_TWITS_PER_BUZZ)

        template_values = {
                            'final_structs': final_structs,
                            }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
