create_entries_table = """
CREATE TABLE IF NOT EXISTS Entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    id_tag    TEXT NOT NULL,   -- tag + timestamp 
    link      TEXT NOT NULL,   -- The repository link
    updated   TEXT NOT NULL,   -- The timestamp of last update
    title     TEXT NOT NULL,   -- The title of the entry
    author    TEXT NOT NULL,   -- Author of the repository/entry
    raw_entry TEXT NOT NULL  -- The raw XML entry.
    
);
"""

select_title_exists = """
SELECT count(title) FROM Entries WHERE title = ?;
"""
"""SELECT count, title = ?"""

insert_entries = """
INSERT INTO Entries (
    id_tag,
    link,
    title,
    updated,
    author,
    raw_entry
) VALUES (?,?,?,?,?,?);
"""
"""id, link, title, updated, author, raw_entry"""


create_gitprofiles_table = """
CREATE TABLE IF NOT EXISTS GitProfiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    url         TEXT    NOT NULL, -- The url the status code refers to 
    http_status INTEGER NOT NULL  -- The http status code (200, 302, etc)
    
);
"""

select_200_codes = """
SELECT url from GitProfiles WHERE http_status = 200;
"""


select_status_code = """
SELECT http_status from GitProfiles WHERE url = ?;
"""
""" http_status, url = ? """


insert_gitprofiles = """
INSERT INTO GitProfiles (
    url,
    http_status
) VALUES (?,?);
"""
"""url, http_status"""

update_status_code_gitprofiles = """
UPDATE GitProfiles
SET http_status = ?
WHERE
    url = ?
;
"""
""" http_status, url """


create_bloggerposts_table = """
CREATE TABLE IF NOT EXISTS Posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    title      TEXT NOT NULL,   -- The title of the entry
    published  TEXT NOT NULL,   -- When the entry was published
    content    TEXT NOT NULL,   -- HTML/text content of the entry
    raw_entry  TEXT NOT NULL   -- raw XML for the entry
    
);
"""

insert_post = """
INSERT INTO Posts (
    title,
    published,
    content,
    raw_entry
) VALUES (?,?,?,?);
"""
"""title, published, content, raw_entry"""

select_post_exists = """
SELECT count(title) FROM Posts WHERE title = ? AND published = ?;
"""
"""SELECT count, title = ?, published = ?"""