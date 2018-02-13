from gmusicapi import Mobileclient
import os

# prerequisites:
# install python with pip: https://www.python.org/downloads/
# install gmusic api using pip: http://unofficial-google-music-api.readthedocs.io/en/latest/usage.html
# get a google app-specific token for 2 factor auth: https://www.google.com/accounts/IssuedAuthSubTokens?hide_authsub=1

# usage:
# follow a few artists, build up your artist/album database (under /artists folder)
# come back on new music friday (or whenever you like) and check for updates/new albums
# in your browser, add whichever albums showed up in the update to your gpm library/playlist that are of interest
# when finished, sync the local database with your gpm library so that it's ready for the next run

username = 'your@email.com'
api_token = 'yourapitoken'
api = Mobileclient()

def main_menu():
    print("\nmain menu:\n")
    print("(f) start following a new artist by name")
    print("(l) list artists being followed")
    print("(u) check for updates to followed artists")
    print("(s) sync the local album database with gpm")
    print("(q) quit")
    user_input = input('\nselection: ')
    selection = user_input.lower()[:1]

    if (selection == 'f'):
        search_artists()
    elif (selection == 'l'):
        list_artists()
    elif (selection == 'u'):
        get_album_updates()
    elif (selection == 's'):
        sync_artists()
    elif (selection == 'q'):
        logout_and_quit()
    else:
        print("unrecognized option: %s" % user_input)
        
    main_menu()
        
def search_artists():
    artist_name = input('\nenter artist name: ')
    results = api.search(artist_name, 9)
    num_results = len(results['artist_hits'])

    if num_results > 1:
        print('\nmore than 1 result for %s - showing %d:\n' % (artist_name, num_results))

        for index in range(num_results):
            artist = results['artist_hits'][index]['artist']
            artist_info = api.get_artist_info(artist['artistId'], True, 0, 0)
            artist_bio = ""
            
            if ('artistBio' in artist_info):
                artist_bio = " - %s..." % artist_info['artistBio'][:60]
            
            print("(%d) %s%s" % (index + 1, artist['name'], artist_bio))

        print("(q) quit to main menu")
        user_input = input('\nselection: ')
        
        if (not user_input or not user_input.isdigit() or len(user_input) > 1):
            print("unrecognized option: %s" % user_input)
            return
            
        selection = user_input.lower()[:1]
        
        if (selection == 'q'):
            return
        
        follow_artist(results['artist_hits'][int(selection) - 1]['artist'])
    elif len(results['artist_hits']) == 1:
        follow_artist(results['artist_hits'][0]['artist'])
    else:
        print("no results")

def follow_artist(artist):
    artist_id = artist['artistId']
    print('\nadded artist: %s (id: %s)' % (artist['name'], artist_id))
    artist_results = api.get_artist_info(artist_id, True, 0, 0)

    if not os.path.exists('artists'):
        os.makedirs('artists')
    
    target = open('artists/%s.dat' % artist_id, 'w')
    target.write(str(artist_results))
    target.close()

def list_artists():
    print("\nartists followed:\n")
    
    for fn in os.listdir('artists'):
        if (fn.endswith('.dat')):
            artist_id = fn.replace('.dat', '')
            target = open('artists/%s.dat' % artist_id, 'r')
            artist_data = eval(target.read())
            target.close()
            print('(id: %s) %s' % (artist_id, artist_data['name']))

    print('\nto unfollow an artist, delete their artist_id.dat file under /artists')
    
def get_album_updates():
    print()
    
    for fn in os.listdir('artists'):
        if (fn.endswith('.dat')):
            get_artist_updates(fn.replace('.dat', ''))
        
def get_artist_updates(artist_id):
    target = open('artists/%s.dat' % artist_id, 'r')
    old_albums = eval(target.read())
    target.close()
    print('checking %s...' % old_albums['name'])
    artist_results = api.get_artist_info(artist_id, True, 0, 0)

    for new_album in artist_results['albums']:
        found_album = False
    
        for old_album in old_albums['albums']:
            if old_album['albumId'] == new_album['albumId']:
                found_album = True
                break

        if not found_album:
            print("    no match for %s" % new_album['name'])

def sync_artists():
    print()
    
    for fn in os.listdir('artists'):
        if (fn.endswith('.dat')):
            sync_albums(fn.replace('.dat', ''))

    print("\ndatabase synced to gpm")

def sync_albums(artist_id):
    target = open('artists/%s.dat' % artist_id, 'r')
    old_albums = eval(target.read())
    target.close()
    print('syncing %s...' % old_albums['name'])
    artist_results = api.get_artist_info(artist_id, True, 0, 0)
    target = open('artists/%s.dat' % artist_id, 'w')
    target.write(str(artist_results))
    target.close()
            
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
main_menu()