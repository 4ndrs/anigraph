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
import sqlite3
import requests
import queries
from sys  import stderr
from yaml import dump as save_yaml, load as load_yaml, CLoader as loader

_version        = 0.01
_client_id      = 8271
_config_file    = 'config.yaml'
_db_name        = 'AniGraph.db'
_config_dir     = os.path.abspath('AniGraph') # TODO: change to standard config dir
_api_url        = 'https://graphql.anilist.co'
_auth_url       = 'https://anilist.co/api/v2/oauth/authorize?client_id='\
                  + str(_client_id) + '&response_type=token'

# Check the config file and load into memory if it exists
def config(conf):
    _cfg = os.path.join(_config_dir, _config_file)
    if os.path.exists(_cfg):
        with open(os.path.join(_cfg)) as file: conf = load_yaml(file, loader)

# Quick check to see if the auth information is in the database
def db_check():
    con = sqlite3.connect(_db_name)
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
    # The configuration consist of the location for the js/html files
    # config files path, and synchronization settings
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
        con = sqlite3.connect(_db_name)
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
    pass

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
