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

get_user_list =\
'''
query ($userName: String, $perChunk: Int, $Chunk: Int) {
  MediaListCollection(userName: $userName, type:ANIME, perChunk: $perChunk,
					  chunk:$Chunk, sort: UPDATED_TIME_DESC){
    hasNextChunk
    lists {
      entries {
        media {
          id
		  episodes
          title {
            romaji
            native
          }
          season
          seasonYear
          genres
          mediaListEntry {
            updatedAt
            score (format: POINT_100)
			status
			progress
          }
        }
      }
    }
  }
}
'''

_get_user_list =\
'''
{
  Page(page: $page, perPage:$perPage) {
    pageInfo {
      hasNextPage
      lastPage
    }
    mediaList (userName:$userName, type:ANIME, sort: ADDED_TIME_DESC){
      media {
        id
        title {
          romaji
          native
        }
        season
        seasonYear
        genres
        mediaListEntry {
          score
        }
      }
    }
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

get_user_name =\
'''
SELECT name FROM auth_user
'''

get_user_token =\
'''
SELECT token FROM auth_user
'''

userdb_get_last_updated =\
'''
SELECT MAX(updated_at) FROM Series
'''

userdb_get_season_id =\
'''
SELECT id FROM Seasons WHERE season = ? AND season_year = ?
'''

userdb_get_status_id =\
'''
SELECT id FROM Status WHERE status = ?
'''

userdb_get_genre_id =\
'''
SELECT id FROM Genres WHERE genre = ?
'''

userdb_insert_status =\
'''
INSERT OR IGNORE INTO Status (status) VALUES (?)
'''

userdb_insert_seasons =\
'''
INSERT OR IGNORE INTO Seasons (season, season_year) VALUES (?, ?)
'''

userdb_insert_genres =\
'''
INSERT OR IGNORE INTO Genres (genre) VALUES (?)
'''

userdb_insert_series =\
'''
INSERT OR REPLACE INTO Series (id, title_romaji, title_native, episodes, progress, score, updated_at,
                               season_id, status_id) VALUES (?,?,?,?,?,?,?,?,?)
'''

userdb_insert_series_and_genres =\
'''
INSERT OR IGNORE INTO Series_and_Genres (series_id, genre_id) VALUES (?, ?)
'''

userdb_initialize =\
'''
CREATE TABLE IF NOT EXISTS Status (
	id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	status          TEXT UNIQUE
);
CREATE TABLE IF NOT EXISTS Seasons (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    season          TEXT,
    season_year     INTEGER,
    UNIQUE (season, season_year)
);

CREATE TABLE IF NOT EXISTS Genres (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    genre           TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Series (
    id INTEGER PRIMARY KEY UNIQUE,
    title_romaji    TEXT,
    title_native    TEXT,
	episodes        INTEGER,
	progress        INTEGER,
    score           INTEGER,
    updated_at      INTEGER,
    season_id       INTEGER,
    status_id       INTEGER
);

CREATE TABLE IF NOT EXISTS Characters (
    id INTEGER PRIMARY KEY UNIQUE,
    name_last       TEXT,
    name_first      TEXT
);

CREATE TABLE IF NOT EXISTS VAs (
    id INTEGER PRIMARY KEY UNIQUE,
    name_last       TEXT,
    name_first      TEXT
);

CREATE TABLE IF NOT EXISTS Series_and_Genres (
    series_id       INTEGER,
    genre_id        INTEGER,
    UNIQUE (series_id, genre_id)
);

CREATE TABLE IF NOT EXISTS Series_and_Characters (
    series_id       INTEGER,
    character_id    INTEGER,
    UNIQUE (series_id, character_id)
);

CREATE TABLE IF NOT EXISTS Characters_and_VAs (
    character_id    INTEGER,
    va_id           INTEGER,
    UNIQUE (character_id, va_id)
);
'''
