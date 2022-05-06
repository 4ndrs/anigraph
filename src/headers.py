#
# headers.py:
#       File for function definitions
#
# Copyright (c) 2022
# Andres Eloy Rivera Garcia
#
# SPDX-License-Identifier: MIT
#
import yaml
from re import findall

_version = 0.01

# Check the config file and load into memory if it exists
def config(conf):
    pass

# Change the config settings
def set_config(conf):
    pass

# Do the first run asking the user if they want to proceed using 
# the default settings or want to personalize the configuration
def first_run(conf, exec_path):
    # The configuration consist of the location for the js/html files
    # config files path, and synchronization settings
    # Use only local paths as the default for the moment
    conf['config_path'] = findall('(.+/)', exec_path)[0]
    conf['save_path']   = conf['config_path']
    pass

# Print a short help message
def print_short_help():
    pass

# Print the extended help
def print_help():
    pass

# Sync the database with upstream
def sync(conf_path):
    pass

# Extract the data from the local database and generate the js/html files
def export(conf_path, save_path):
    pass

# Open the js/html files with the web browser using Python's webbrowser module
def open(config_path, save_path):
    pass

# Delete all user specific data (database tables & js/html files)
def delete(config_path, save_path):
    pass

# Print version information
def version():
    pass
