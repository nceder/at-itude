#!/usr/bin/env python

""" scores data gathered from twitter

    nrc 29/11/2014

"""


import sys

sys.setdefaultencoding("utf-8")
import site
import os
import csv

import json
from collections import Counter
from textblob import TextBlob

porn_spam = set(['escort', 'porn', '#porn', '#anal' ])

slurs = set(['shemale', 'tranny', 'trannie', 'fag', 'faggot'])

# filter_list = set(['girl', 'women', 'woman', 'girls', 'female' 'genderfluid', 'butch',  'dyke','lesbian', 'lezza','orientation', 'gender'])

filter_list = set(['gay', 'lesbian', 'bi', 'trans','queer', 'transgender', 'bisexual', 'butch', 'dyke', 'fag', 'faggot', 'homo', 'drag queen', 'drag king', 'tranny', 'transsexual', 'LGBT', 'genderqueer', 'homophobic', 'homophobia', 'homosexual', 'intersex', 'ladyboy', 'lesbo', 'sissy', 'pro-gay', 'anti-gay', 'shemale', 'transvestite', 'sexual minority', 'genderfluid', 'arse bandit', 'homophobia', 'bi-curious', 'butch', 'lezza', 'nancy boy', 'poofta', 'equal', 'pride', 'gaymer', 'panic', 'orientation', 'gender'])


if __name__ == '__main__':

    data_file = csv.reader(open(sys.argv[1], "rbU"))
    out_file_pos = csv.writer(open(sys.argv[2], "wb"))
    out_file_neu = csv.writer(open(sys.argv[2], "wb"))
    out_file_neg = csv.writer(open(sys.argv[2], "wb"))


    out_file_pos.writerow(['polarity','subjectivity','longitude','latitude'])
    out_file_neu.writerow(['polarity','subjectivity','longitude','latitude'])
    out_file_neg.writerow(['polarity','subjectivity','longitude','latitude'])
    

    for row in data_file:
        try:
            blob = TextBlob(row[0].lower().encode('utf-8'))
            word_set = set(blob.words)
        except:
            print row[0]
            continue
        if not word_set & filter_list:
            continue
        #if word_set & porn_spam:
        #    continue
        print row[0]
        score = blob.sentiment
        polarity, subjectivity = score
        longitude, lat = (None, None)
        #if word_set & slurs:
        #    polarity -= 0.5
        try:
            if row[2]:
                row[2] = json.loads(row[2])
                print row[2]
                print tuple(row[2]['coordinates'])
                if row[2]['type'] == "Point":
                    longitude, lat = tuple(row[2]['coordinates'])
                else:
                    longitude, lat = row[2]['coordinates'][0][0]
            elif row[3]:
                row[3] = json.loads(row[3])
                print row[3]
                print tuple(row[3]['coordinates'])
                if row[3]['type'] == "Point":
                    lat, longitude = tuple(row[3]['coordinates'])
                else:
                    lat, longitude = row[3]['coordinates'][0][0]
            elif row[4]:
                print row[4]
                longitude, lat = row[4]['bounding_box']['coordinates'][0][0]
            else:
                continue
        except:
            pass
        new_row = [polarity, subjectivity, longitude, lat]
        print new_row
        if not longitude or not lat:
            continue
        if new_row[0] > 0.2:
            out_file_pos.writerow(new_row)
        if new_row[0] < -0.2:
            out_file_neg.writerow(new_row)
        else:
            out_file_neu.writerow(new_row)
