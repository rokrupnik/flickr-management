"""
    A script that recursively iterates given folder and for every directory that contains
    photos creates a Flickr photoset, uploads contained photos and
    adds them to the created photoset.
"""

####################################################################################################
# Removing annoying warnings

import requests
from requests.packages.urllib3.exceptions import InsecurePlatformWarning, SNIMissingWarning
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

####################################################################################################

####################################################################################################
# Init time measurements

import time
import datetime

START = time.time()
CHECKPOINT = time.time()

def print_time(checkpoint):
    end = time.time()

    s = end - START
    h = int(s / 3600)
    s = s - (h * 3600)
    m = int(s / 60)
    s = s - (m * 60)
    print 'current time: ' + str(datetime.datetime.now().time()) +\
        ' || time elapsed: %d hours, %d minutes and %d seconds' % (h, m, s)

    s = end - checkpoint
    h = int(s / 3600)
    s = s - (h * 3600)
    m = int(s / 60)
    s = s - (m * 60)
    print ' || time for last set: %d hours, %d minutes and %d seconds' % (h, m, s)
####################################################################################################

####################################################################################################
# Init flickrapi

import os
import sys
import flickrapi
from flickr_account import *

# Fileclass for following the upload progress
class FileWithCallback(object):
    def __init__(self, filename, callback):
        self.file = open(filename, 'rb')
        self.callback = callback
        # the following attributes and methods are required
        self.len = os.path.getsize(filename)
        self.fileno = self.file.fileno
        self.tell = self.file.tell
        self.old_progress = -1

    def read(self, size):
        if self.callback:
            progress = self.tell() * 100 // self.len
            self.callback(progress, self.old_progress)
            self.old_progress = progress
        return self.file.read(size)

def callback(progress, old_progress):
    if (progress != old_progress):
        print str(progress) + '%',

ALLOWED_FILETYPES = ('png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'raw', 'mp4', 'mov', 'avi', 'vob', '3gp')

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
flickr.authenticate_via_browser(perms='write')
####################################################################################################

####################################################################################################
# Init walk_dir

walk_dir = sys.argv[1]

print 'walk_dir = ' + walk_dir

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print 'walk_dir (absolute) = ' + os.path.abspath(walk_dir)
####################################################################################################

####################################################################################################
# Actual directory iteration and upload

for root, subdirs, files in os.walk(walk_dir):
    print '--\nroot = ' + root

    # sort files and subdirs by name
    files = sorted(files)

    photoset_id = 0

    for filename in files:
        file_path = os.path.join(root, filename)
        # upload only photos and video
        if not(filename.lower().endswith(ALLOWED_FILETYPES)):
            print '\terror: wrong file type in file %s (full path: %s)\n\t' % (filename, file_path),
            continue

        if (photoset_id == 0):
            #####################################
            # Photoset creation

            # TODO: check if photoset exist and then update it ALSO check if photo with same
            # title exists

            # upload primary photo and create photoset
            print '\tuploading primary photo: %s (full path: %s)\n\t' % (filename, file_path),

            try:
                fileobj = FileWithCallback(file_path, callback)
                rsp = flickr.upload(
                    title=filename,
                    filename=filename,
                    fileobj=fileobj,
                    is_public=0,
                    format='xmlnode'
                )
                primary_photo_id = rsp.photoid[0].text
                print '\n\tuploaded primary photo with id: ' + primary_photo_id

                print '\tcreating photoset with title ' + os.path.split(root)[1]
                rsp = flickr.photosets.create(
                    title=os.path.split(root)[1],
                    primary_photo_id=primary_photo_id
                )
                photoset_id = rsp['photoset']['id']
                print '\tcreated photoset with id ' + photoset_id

            except Exception, e:
                print '\n\t', e
            #####################################
        else:
            #####################################
            # Uploading other photos
            # and adding them to created photoset
            try:

                print '\tuploading file %s (full path: %s)\n\t' % (filename, file_path),

                # upload photos and add them to the photoset
                fileobj = FileWithCallback(file_path, callback)
                rsp = flickr.upload(
                    title=filename,
                    filename=filename,
                    fileobj=fileobj,
                    is_public=0,
                    format='xmlnode'
                )
                photo_id = rsp.photoid[0].text
                print '\n\tphoto_id: ' + photo_id,
                rsp = flickr.photosets.addPhoto(photoset_id=photoset_id, photo_id=photo_id)
                print 'status: ', rsp['stat']

            except Exception, e:
                print '\n\t', e
            #####################################

    # Print all subdirs
    for subdir in subdirs:
        print '\t- subdirectory ' + subdir

    print_time(CHECKPOINT)
    CHECKPOINT = time.time()

print 'Upload completed.'
####################################################################################################
