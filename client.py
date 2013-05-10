import cgi
import datetime
import jinja2
import os
import urllib
import json
import webapp2

def sync_twits(category, address, NUMBER_PER_PAGE):

    """
    :param category:
    :param address:
    :param NUMBER_PER_PAGE:
    :return:
    """
    
    geo_url = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&sensor=true'
    geo_json = json.load(urllib.urlopen(geo_url))
    lat = geo_json['results'][0]['geometry']['location']['lat']
    lng = geo_json['results'][0]['geometry']['location']['lng']
    twi_url = 'http://search.twitter.com/search.json?q=' + category + \
                 '&rpp=' + NUMBER_PER_PAGE + '&geocode=' \
                 + str(geo_json['results'][0]['geometry']['location']['lat']) + ',' \
                 + str(geo_json['results'][0]['geometry']['location']['lng']) + ',' \
                 + '500mi' + '&include_entities=true&result_type=mixed'
    result = [json.loads(urllib.urlopen(twi_url).read())['results']]
    print twi_url
    # print json.loads(urllib.urlopen(twi_url).read())['next_page']
    try:
        page = 0
        while page < 6:

            # print type(json.loads(urllib.urlopen(twi_url).read())['results'])
            # print json.loads(urllib.urlopen(twi_url).read())['results']
            templist = json.loads(urllib.urlopen(twi_url).read())['results']
            result.append(templist)
            twi_url = 'http://search.twitter.com/search.json' +\
                    json.loads(urllib.urlopen(twi_url).read())['next_page']
            page += 1
            # print page
    except:
        pass
    # print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', result
    return result