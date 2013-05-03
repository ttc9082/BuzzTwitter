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
    results = db.TextProperty()
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
        key_name = category + address
        twitters = db.GqlQuery("SELECT * "
                                "FROM twitter "
                                "WHERE ANCESTOR IS :1 "
                                "ORDER BY date DESC LIMIT 10",
                                twitter_key(key_name))
        d = address.split(' ')
        s = ''
        for word in d:
            if s == '':
                s = word
            else:
                s = s + '+' + word
        geo_url = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + s + '&sensor=true'
        geo_json = json.load(urllib.urlopen(geo_url))
        lat = geo_json['results'][0]['geometry']['location']['lat']
        lng = geo_json['results'][0]['geometry']['location']['lng']
        twi_url = 'http://search.twitter.com/search.json?q=' + category + \
                     '&rpp=5&geocode=' \
                     + str(geo_json['results'][0]['geometry']['location']['lat']) + ',' \
                     + str(geo_json['results'][0]['geometry']['location']['lng']) + ',' \
                     + '500mi' + '&include_entities=true&result_type=mixed&lang=en'

        twi = twitter(parent=twitter_key(key_name))
        twi.results = urllib.urlopen(twi_url).read()
        twi.put()
        twi_json = json.load(twitters[0].results)
        twitest = twi_json['results'][1]

        template_values = {
                            'lat': lat,
                            'lng': lng,
                            'twitest': twitest,
                            }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
'''
        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))
'''


app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
