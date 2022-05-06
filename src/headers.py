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
from sys  import stderr
from yaml import dump as save_yaml, load as load_yaml

_version        = 0.01
_config_file    = 'config.yaml'
_config_dir     = os.path.abspath('AniGraph') # TODO: change to standard config dir

# Check the config file and load into memory if it exists
def config(conf):
    pass

# Change the config settings
def set_config(conf):
    pass

# Do the first run asking the user if they want to proceed using 
# the default settings or want to personalize the configuration
def first_run(conf):
    # The configuration consist of the location for the js/html files
    # config files path, and synchronization settings
    # Use only local paths as the default for the moment
    conf['config_path'] = _config_dir
    conf['save_path']   = conf['config_path']

    if not os.path.exists(conf['config_path']):
        try: os.mkdir(conf['config_path'])
        except Exception as err:
            print('Unable to create the config dir: %s' %err, file=stderr)
            exit(127)

    if not os.path.exists(conf['save_path']):
        try: os.mkdir(conf['save_path'])
        except Exception as err:
            print('Unable to create the save dir: %s' %err, file=stderr)
            exit(126)

    with open(os.path.join(conf['config_path'], _config_file), 'w') as file:
        save_yaml(conf, file)

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
