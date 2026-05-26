create_entries_table = """
CREATE TABLE IF NOT EXISTS Entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    id_tag  TEXT NOT NULL, -- tag + timestamp 
    link    TEXT NOT NULL,        -- The repository link
    updated TEXT NOT NULL,        -- The timestamp of last update
    title   TEXT NOT NULL,        -- The title of the entry
    author  TEXT NOT NULL,        -- Author of the repository/entry
    raw_entry TEXT NOT NULL       -- The raw XML entry.
    
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