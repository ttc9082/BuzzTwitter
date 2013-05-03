import cgi
import datetime
import jinja2
import os



import urllib
import json
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action="/sign?%s" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
    <hr>
    <form>Guestbook name: <input value="%s" name="guestbook_name">
    <input type="submit" value="switch"></form>
  </body>
</html>
"""

class twitter(db.Model):
    results = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

def twitter_key(twitter_name=None):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return db.Key.from_path('twitter', twitter_name or 'default')

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        category = self.request.get('category')
        address = self.request.get('location')
        geourl = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + '1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=true'
        get = urllib.urlopen(geourl)
        output_json = json.load(get)
        lat = output_json['results'][0]['geometry']['location']['lat']
        lng = output_json['results'][0]['geometry']['location']['lng']
        '''
        key_name = category + address
        self.response.write(category)
        twi = twitter(parent=twitter_key(key_name))
        twi.results = self.request.get('content')
        twi.put()
        twitters = db.GqlQuery("SELECT * "
                                "FROM twitter "
                                "WHERE ANCESTOR IS :1 "
                                "ORDER BY date DESC LIMIT 10",
                                twitter_key(key_name))
        twitters'''
        template_values = {
            'lat': lat,
            'lng': lng,    
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)