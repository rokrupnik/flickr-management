# -*- coding: utf-8 -*-
"""
    A script that downloads the list of all photosets, orders them by title and
    then uploads the new photosets order on your flickr account.
"""

import sys

# Removing annoying warnings

import requests
from requests.packages.urllib3.exceptions import InsecurePlatformWarning, SNIMissingWarning
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

# Init flickrapi

import flickrapi
from flickr_account import *

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
flickr.authenticate_via_browser(perms='delete')

# Get and sort photosets

sets = flickr.photosets.getList(user_id=user_id)['photosets']['photoset']

sorted_sets = sorted(sets, key=lambda set: set['title']['_content'], reverse=True)

sorted_sets_ids = [set['id'] for set in sorted_sets]

print '\n------------------------------before-----------------------------------\n'
for set_o in sets:
    print unicode(set_o['title']['_content']).encode(sys.stdout.encoding, errors='replace')
print '\n------------------------------after------------------------------------\n'
for set_s in sorted_sets:
    print unicode(set_s['title']['_content']).encode(sys.stdout.encoding, errors='replace')

flickr.photosets.orderSets(photoset_ids=','.join(sorted_sets_ids))
