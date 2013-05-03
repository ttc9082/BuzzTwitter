import cgi
import datetime
import jinja2
import os
import urllib
import json
import webapp2

def sync_twits(category, address, NUMBER_PER_PAGE):
    geo_url = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&sensor=true'
    geo_json = json.load(urllib.urlopen(geo_url))
    lat = geo_json['results'][0]['geometry']['location']['lat']
    lng = geo_json['results'][0]['geometry']['location']['lng']
    twi_url = 'http://search.twitter.com/search.json?q=' + category + \
                 '&rpp=' + NUMBER_PER_PAGE + '&geocode=' \
                 + str(geo_json['results'][0]['geometry']['location']['lat']) + ',' \
                 + str(geo_json['results'][0]['geometry']['location']['lng']) + ',' \
                 + '500mi' + '&include_entities=true&result_type=mixed'
    return urllib.urlopen(twi_url).read()