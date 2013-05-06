import cgi
import datetime
import jinja2
import os
import urllib
import json
import webapp2

import random

def afinn_sentiment(myString):
    afinn = dict(map(lambda (k,v): (k,int(v)), [ line.split('\t') for line in open("AFINN-111.txt") ]))
    score = sum(map(lambda word: afinn.get(word, 0), myString.lower().split()))
    return score

def generate_struct(twitest, buzz_words, NUMBER_OF_TWITS_PER_BUZZ):
    final_struct = []
    for buzzWord in buzz_words:
        temp_dict = {}
        temp_dict['buzz_word'] = buzzWord
        temp_dict['matched_twits'] = []
        temp_array = ""
        for twit in twitest:
            if buzzWord.lower() in twit["text"].lower():
                temp_dict['matched_twits'].append(twit)
                temp_array = temp_array + twit["text"]
        # print "______________________________________________________________________________________________________"
        # print len(temp_array.split(" "))

        temp_dict['sentiment'] = afinn_sentiment("temp_array")
        min_num = min( len(temp_dict['matched_twits']), NUMBER_OF_TWITS_PER_BUZZ )
        temp_dict['sample'] = random.sample(temp_dict['matched_twits'], min_num)
        final_struct.append(temp_dict)
    return final_struct


