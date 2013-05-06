import cgi
import datetime
import jinja2
import os
import urllib
import json
import webapp2
from google.appengine.ext import db
from google.appengine.api import users

class twitter(db.Model):
    address = db.StringProperty()
    category = db.StringProperty()
    results = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True)

def has_key(address, category):
    q = twitter.all()
    q.filter("address =", address)
    q.filter("category =", category)
    q.order("-address")
    if q.fetch(1):
        print '+====================================+'
        print 'cache found!'
        # print '+====================================+'
        return q.fetch(1)[0]
    else:
        return False

def retrieve_data(address, category):
    q = twitter.all()
    q.filter("address =", address)
    q.filter("category =", category)
    q.order("-address")
    print '+====================================+'
    print 'return results!'
    # print '+====================================+'
    return q.fetch(1)[0].results

def store_data(address, category, jsonstr):
    twi = twitter(
                address=address,
                category=category,
                results=jsonstr)
    twi.put()
    print '+====================================+'
    print 'cache saved!'
    # print '+====================================+'
    return True

