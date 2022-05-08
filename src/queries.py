#
# queries.py:
#       File for variables containing SQL & API queries
#
# Copyright (c) 2022
# Andres Eloy Rivera Garcia
#
# SPDX-License-Identifier: MIT
#

# API queries
get_user =\
'''
{
  Viewer {
    id
    name
    
  }
}
'''

# SQLite queries
create_auth_user_table =\
'''
CREATE TABLE IF NOT EXISTS auth_user (
    id INTEGER UNIQUE,
    name TEXT,
    token TEXT
)
'''
save_user_auth =\
'''
INSERT INTO auth_user (id, name, token) VALUES (?, ?, ?)
'''
