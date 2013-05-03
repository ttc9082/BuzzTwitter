import cgi
import datetime
import jinja2
import os
import urllib
import json
import webapp2

def has_key(clause):
    count = 0
    # TODO:

    # select *.count from ...
    return count

def retrieve_data(clause):
    return_string = ""
    # TODO:

    # select string
    # where key = clause
    # from ...
    return return_string

def store_data(clause, twitest):
    # TODO:

    # INSERT INTO table_name (column1,column2,column3,...)
    # VALUES (value1,value2,value3,...)
    return



'''
greeting.content = self.request.get('content')
greeting.put()

query_params = {'guestbook_name': guestbook_name}
self.redirect('/?' + urllib.urlencode(query_params))

key_name = category + address
self.response.write(category)
twi = twitter(parent=twitter_key(key_name))
twi.results = urllib.urlopen(twi_url).read()
twi.put()
twitters = db.GqlQuery("SELECT * "
                                "FROM twitter "
                                "WHERE ANCESTOR IS :1 "
                                "ORDER BY date DESC LIMIT 10",
                                twitter_key(key_name))
twitters'''