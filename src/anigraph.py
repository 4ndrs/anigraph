#!/usr/bin/env python3
# 
# anigraph.py:
#       Main executable, command line options here
#
# Copyright (c) 2022
# Andres Eloy Rivera Garcia
#
# SPDX-License-Identifier: MIT
#
from sys import argv, stderr, platform
from re import findall
import headers as ani

# Can only test on Linux at the moment
# Avoid running on other platforms as precaution
if platform != 'linux':
    print('Unrecognized OS/platform', file=stderr)
    exit(-1)

# Load the config file & check the DB
conf  = dict()
db_ok = False
ani.config(conf)
db_ok = ani.db_check(conf.get('config_path', -1))

# If there is no config file, assume it's the first run
if len(conf) < 1: ani.first_run(conf, db_ok)

# Arguments:
#   --help    or -h - to print the extended help
#   --config  or -c - to change configuration settings
#   --sync    or -s - to synchronize database
#   --export  or -x - to generate js/html
#   --open    or -o - to open the js/html (generate & open if no js/html or old data)
#   --delete  or -d - to delete local account data
#   --version or -v - to print version information
arguments = ['help', 'config', 'sync', 'export', 'open', 'delete', 'version',
             'h', 'c', 's', 'x', 'o', 'd', 'v']

# Only the first argument will be parsed for now
try:    arg = findall('^-[-]?([a-z]+)', argv[1])[0]
except: arg = None

if len(argv) < 2:
    # If no arguments are given, just open the generated js/html files
    # if the files have not been generated yet, and/or the database has not
    # been sync'd, this will sync the database and generate the js/html files
    # and proceed to run them
    ani.open_stats(conf['config_path'], conf['save_path'])
elif arg is None:
    print('ERROR: Unrecognized argument format: %s\n' %argv[1], file=stderr)
    ani.print_short_help()
    exit(2)
elif arg not in arguments:
    print('ERROR: Unrecognized argument: %s\n' %arg, file=stderr)
    ani.print_short_help()
    exit(3)

if arg == 'help'    or arg == 'h': ani.print_help()
if arg == 'config'  or arg == 'c': ani.set_config(conf)
if arg == 'sync'    or arg == 's': ani.sync_db(conf['config_path'])
if arg == 'export'  or arg == 'x': ani.export_stats(conf['config_path'], conf['save_path'])
if arg == 'open'    or arg == 'o': ani.open_stats(conf['config_path'], conf['save_path'])
if arg == 'delete'  or arg == 'd': ani.delete(conf['config_path'], conf['save_path'])
if arg == 'version' or arg == 'v': ani.version()

exit(0)
