#
# headers.py:
#       File for function definitions
#
# Copyright (c) 2022
# Andres Eloy Rivera Garcia
#
# SPDX-License-Identifier: MIT
#
import os
import time
import sqlite3
import queries
import requests
from sys  import stderr
from urllib.parse import urlencode
from yaml import dump as save_yaml, load as load_yaml, CLoader as loader

_version        = 0.01
_client_id      = 8271
_config_file    = 'config.yaml'
_db_name        = 'AniGraph.db'
_config_dir     = os.path.abspath('AniGraph') # TODO: change to standard config dir
_api_url        = 'https://graphql.anilist.co'
_req            = {'client_id':_client_id, 'response_type':'token'}
_auth_url       = 'https://anilist.co/api/v2/oauth/authorize?' + urlencode(_req)

# Check the config file and load into memory if it exists
def config(conf):
    _cfg = os.path.join(_config_dir, _config_file)
    if os.path.exists(_cfg):
        with open(os.path.join(_cfg)) as file: conf = load_yaml(file, loader)

# Quick check to see if the auth information is in the database
def db_check(config_path):
    if config_path == -1: con = sqlite3.connect(os.path.join(_config_dir, _db_name))
    else: con = sqlite3.connect(os.path.join(config_path, _db_name))
    cur = con.cursor()
    try:
        cur.execute('SELECT token FROM auth_user;')
        if len(cur.fetchone()) < 1:
            con.close()
            return False
        con.close()
        return True
    except:
        con.close()
        return False

# Change the config settings
def set_config(conf):
    pass

# Do the first run asking the user if they want to proceed using 
# the default settings or want to personalize the configuration
def first_run(conf, db_ok):
    # Use only local paths as the default for the moment
    conf['config_path'] = _config_dir
    conf['save_path']   = conf['config_path']

    if not os.path.exists(conf['config_path']):
        try: os.mkdir(conf['config_path'])
        except Exception as err:
            print('Unable to create the config dir:', err, file=stderr)
            exit(127)

    if not os.path.exists(conf['save_path']):
        try: os.mkdir(conf['save_path'])
        except Exception as err:
            print('Unable to create the save dir:', err, file=stderr)
            exit(126)

    with open(os.path.join(conf['config_path'], _config_file), 'w') as file:
        save_yaml(conf, file)

    # Ask the user to generate an auth token to use for authenticated queries
    if not db_ok:
        con = sqlite3.connect(os.path.join(conf['config_path'], _db_name))
        cur = con.cursor()
        cur.execute(queries.create_auth_user_table)
        print('An AniList authorization token is necessary to proceed. ' \
               'Navigate to the following link, and paste the token generated ' \
               'by the server, below.\nLink:', _auth_url)
        while True:
            token = input('Token: ')
            if len(token) < 1:
                print('No token provided')
                continue
            else:
                token = token.strip()
                print('Trying to get user information...')
                request = requests.post(_api_url, json={'query': queries.get_user},
                          headers = {'Authorization': 'Bearer ' + token})
                if request.status_code != 200:
                    print('Could not get user information, error code:', request.status_code)
                    continue
                uname = request.json()['data']['Viewer']['name']
                uid   = request.json()['data']['Viewer']['id']
                print('User information retrieved\nName:', uname, '\nID:', uid)
                print('Saving auth information to the database...')
                cur.execute(queries.save_user_auth, (uid, uname, token))
                break
        con.commit()
        con.close()
        # TODO: implement sync function and launch it here

# Print a short help message
def print_short_help():
    pass

# Print the extended help
def print_help():
    pass

# Sync the database with upstream
def sync_db(conf_path):
    print('Processing sync...')
    con = sqlite3.connect(os.path.join(conf_path, _db_name))
    cur = con.cursor()

    _chunk   	    = 1 # Current chunk
    _sync_perchunk  = 10 # Items per chunk for normal sync
    _full_perchunk  = 100 # Items per chunk for first  sync
    _username       = cur.execute(queries.get_user_name).fetchone()[0]
    _token          = cur.execute(queries.get_user_token).fetchone()[0]
    _userdb         = _username + '.db' # Database for user's list

    con.close()
    con = sqlite3.connect(os.path.join(conf_path, _userdb))
    cur = con.cursor()

    # Schema plan:
    # https://docs.google.com/spreadsheets/d/1nO6fvxYeIJ6kgsiaeAohVpNf6MuaBRnZHz8imMolq_4
    cur.executescript(queries.userdb_initialize)
    con.commit()

    _db_last_updated = cur.execute(queries.userdb_get_last_updated).fetchone()[0]
    if _db_last_updated is None: _perchunk = _full_perchunk # For big syncs, only the first time when no DB
    else:                        _perchunk = _sync_perchunk # Checking small changes little by little

    if _perchunk == _full_perchunk: print('No local data found. Trying a full sync.', end='', flush=True)
    else: print('Trying a normal sync.', end='', flush=True)

    count = 0
    while True:
        variables = {
            'Chunk'     : _chunk,
            'perChunk'  : _perchunk,
            'userName'  : _username
        }

        request = requests.post(_api_url, json={'query': queries.get_user_list, 'variables': variables},
                                headers = {'Authorization': 'Bearer ' + _token})
        _upstream_last_updated =\
        request.json()['data']['MediaListCollection']['lists'][0]['entries'][0]['media']['mediaListEntry']['updatedAt']
        _has_nextchunk = request.json()['data']['MediaListCollection']['hasNextChunk']
        _rate_limit_remaining = request.headers['X-RateLimit-Remaining']
        _status_code = request.status_code

        if int(_rate_limit_remaining) < 5: time.sleep(60) # Avoid going over the rate limit

        if _status_code != 200:
            print('Unhandled status code:', _status_code)
            break

        # Check if there has been any changes upstream before sync
        if _perchunk == _sync_perchunk and _db_last_updated == _upstream_last_updated:
            print('\nLocal data is up to date with upstream')
            break

        # Now we can sync, or pull the full list from upstream
        for listx in request.json()['data']['MediaListCollection']['lists']:
            for entry in listx['entries']:
                entry = entry['media']
                _id             = entry['id']
                _episodes       = entry['episodes']
                _title_romaji   = entry['title']['romaji']
                _title_native   = entry['title']['native']
                _season         = entry['season']
                _season_year    = entry['seasonYear']
                _genres         = entry['genres']
                _score          = entry['mediaListEntry']['score']
                _status         = entry['mediaListEntry']['status']
                _progress       = entry['mediaListEntry']['progress']
                _updated_at     = entry['mediaListEntry']['updatedAt']

                # For debugging purposes
                #print('id:', _id)
                #print('episodes:', _episodes)
                #print('title:', _title_romaji)
                #print('title:', _title_native)
                #print('season:', _season)
                #print('season:', _season_year)
                #print('genres:', _genres)
                #print('score:', _score)
                #print('status:', _status)
                #print('progress:', _progress)
                #print('updated:', _updated_at)
                    #print('Entry number: %i\nID: %i\nUpdated at: %i\nTitle: %s\n日本語: %s\n'\
                #      'Season: %s %i\nScore: %i\nStatus: %s\nProgress: %s\nEpisodes: %s\n'\
                #      % (count, _id, _updated_at, _title_romaji, _title_native, _season, _season_year,
                #         _score, _status, _progress, _episodes))

                if _season is None:
                    _season      = 'null_season'
                    _season_year = 0

                # Update the database
                cur.execute(queries.userdb_insert_status,  (_status,))
                cur.execute(queries.userdb_insert_seasons, (_season, _season_year))
                for _genre in _genres: cur.execute(queries.userdb_insert_genres, (_genre,))

                # Let's pull this entry's status_id, and season_id
                _season_id = cur.execute(queries.userdb_get_season_id, (_season, _season_year)).fetchone()[0]
                _status_id = cur.execute(queries.userdb_get_status_id, (_status,)).fetchone()[0]

                cur.execute(queries.userdb_insert_series, (_id, _title_romaji, _title_native,
                                                           _episodes, _progress, _score,
                                                           _updated_at, _season_id, _status_id))
                # Series and Genres connections
                for _genre in _genres:
                    _genre_id = cur.execute(queries.userdb_get_genre_id, (_genre,)).fetchone()[0]
                    cur.execute(queries.userdb_insert_series_and_genres, (_id, _genre_id))

                count += 1

        # HDD too slow, moved commit here
        con.commit()
        print('.', end='', flush=True)
        if not _has_nextchunk: break
        else:  _chunk += 1
        time.sleep(1)
    con.close()
    print('\nProcessed', count, 'entries')

# Extract the data from the local database and generate the js/html files
def export_stats(conf_path, save_path):
    pass

# Open the js/html files with the web browser using Python's webbrowser module
def open_stats(config_path, save_path):
    pass

# Delete all user specific data (database tables & js/html files)
def delete(config_path, save_path):
    pass

# Print version information
def version():
    pass
