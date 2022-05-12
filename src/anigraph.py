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

arguments = ('help', 'config', 'sync', 'export', 'open', 'delete', 'version',
             'top', 'h', 'c', 's', 'x', 'o', 'd', 'v', 't')

try:    arg = findall('^-[-]?([a-z]+)', argv[1])[0]
except: arg = None

if len(argv) < 2:
    # If no arguments are given, just open the generated js/html files
    # if the files have not been generated yet, and/or the database has not
    # been sync'd, this will sync the database and generate the js/html files
    # and proceed to run them
    ani.open_stats(conf['config_path'], conf['save_path'])
elif arg is None:
    print(f'Unrecognized argument format: {argv[1]}\n', file=stderr)
    ani.print_short_help()
    exit(2)
elif arg not in arguments:
    print(f'Unrecognized argument: {arg}\n', file=stderr)
    ani.print_short_help()
    exit(3)

if arg == 'help'    or arg == 'h': ani.print_help()
if arg == 'config'  or arg == 'c': ani.set_config(conf)
if arg == 'sync'    or arg == 's': ani.sync_db(conf['config_path'])
if arg == 'export'  or arg == 'x': ani.export_stats(conf['config_path'], conf['save_path'])
if arg == 'open'    or arg == 'o': ani.open_stats(conf['config_path'], conf['save_path'])
if arg == 'delete'  or arg == 'd': ani.delete(conf['config_path'], conf['save_path'])
if arg == 'version' or arg == 'v': ani.version()

# Usage: ./% -t 10 rated series
#        ./% -t 10 rated genres
#        ./% -t 10 rated VA participation # VAs with the most rated series
#        ./% -t 10 watched genres
#        ./% -t 10 VA participation       # VAs frequency in series
if arg == 'top' or arg == 't':
    if len(argv) < 4:
        print('Not enough arguments', file=stderr)
        exit(4)

    try:    top_n = int(argv[2])
    except:
        print('Invalid number:', argv[2], file=stderr)
        exit(5)

    reqs = ('rated series', 'rated genres', 'rated va participation', 'watched genres',
            'va participation', 'rs', 'rg', 'rvp', 'wg', 'vp')
    req0 = ''
    for word in argv[3:]: req0 += word + ' '
    req = req0.rstrip().lower()

    if req not in reqs:
        print('Request not understood: ', req0, file=stderr)
        exit(5)

    if req == 'rated series'            or req == 'rs': ani.print_stuff(conf['config_path'],  'rs',  top_n)
    if req == 'rated genres'            or req == 'rg': ani.print_stuff(conf['config_path'],  'rg',  top_n)
    if req == 'rated va participation'  or req == 'rvp': ani.print_stuff(conf['config_path'], 'rvp', top_n)
    if req == 'watched genres'          or req == 'wg': ani.print_stuff(conf['config_path'],  'wg',  top_n)
    if req == 'va participation'        or req == 'vp': ani.print_stuff(conf['config_path'],  'vp',  top_n)

exit(0)
