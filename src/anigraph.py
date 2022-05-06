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
from sys import argv
import headers as ani

# Load the config file
conf = dict()
ani.config(conf)

# If there is no config file, assume it's the first run
if len(conf) < 1: ani.first_run(conf)
