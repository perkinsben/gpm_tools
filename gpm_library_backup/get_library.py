from gmusicapi import Mobileclient
from operator import itemgetter
from csv import DictWriter
import os

username = 'your@email.com'
api_token = 'your api token'
library_filename = 'library'
api = Mobileclient()
content = []

def get_all_songs():
    print("\nretrieving library..."),
    all_songs = api.get_all_songs()

    for x in range(len(all_songs)):
        gatherList = {
            "album":       all_songs[x].get('album').encode('utf-8', errors='ignore'),
            "artist":      all_songs[x].get('artist').encode('utf-8', errors='ignore'),
            "name":        all_songs[x].get('title').encode('utf-8', errors='ignore'),
            "trackNumber": all_songs[x].get('trackNumber'),
            "playCount":   all_songs[x].get('playCount')
            }
        content.append(gatherList)

def save_library():
    temp = sorted(content, key = itemgetter('trackNumber'))
    temp = sorted(temp,    key = itemgetter('album'))
    temp = sorted(temp,    key = itemgetter('artist'))

    # library_filename = raw_input('save file as (do not include .csv or any extension!)\n: ')
    try:
        with open(library_filename + '.csv', 'w') as outfile:
            print ("exporting library to CSV format"),
            writer = DictWriter(outfile, ('artist', 'album', 'trackNumber', 'name','playCount'))
            writer.writeheader()
            writer.writerows(temp)
            print ('\'' + str(library_filename) + str('.csv') + '\' saved in current directory')
    except IOError:
        sys.exit("invalid filename!")

def login_to_gpm():
    logged_in = api.login(username, api_token, Mobileclient.FROM_MAC_ADDRESS)
    
    if (logged_in):
        print("logged in as %s" % username)
    else:
        print("login failed - verify username and api token in %s" % __file__)
        quit()

def logout_and_quit():
    logged_out = api.logout()
    print("\nlogged out")
    quit()
    
login_to_gpm()
get_all_songs()
save_library()
logout_and_quit()