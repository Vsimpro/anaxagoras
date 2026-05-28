import time, requests
import xml.etree.ElementTree as ET

from html import unescape

from src.msg_relay import initialize_apprise

from database import main as sql3
from database import queries



# Global Variables
POST_OFFICE = None
INTERVAL    = 60


def notify_new_post( title ):
    POST_OFFICE.notify(
        title = "## New post detected on blogspot!",
        body  = f"`deadeclipse666.blogspot.com`\n posted with the title `{ title }.`"
    )
    
    
def notify_request_error( status_code ):
    POST_OFFICE.notify(
        title = "## Possible BlogSpot ban!",
        body  = f"`deadeclipse666.blogspot.com`\n is now giving `{status_code}`"
    )


def store( title, published, content, raw_entry):
    conn = sql3.query_database(
            queries.select_post_exists,
            (title, published)
    )

    if not conn:
        return

    # Check if post exists
    exists : int = conn[ 0 ][ 0 ]

    # Stored! No need to continue.
    if exists == 1:
        return

    # Send a notification that a new repo has appeared.
    notify_new_post( title )

    # .. and store the data.
    sql3.insert_data(
        queries.insert_post,
        (title, published, content, raw_entry)
    )


def get_xml():
    response = requests.get( "https://deadeclipse666.blogspot.com/feeds/posts/default" )
    
    # Something is wrong/ changed. Notify the user and exit.
    if 200 != response.status_code:
        notify_request_error( response.status_code )
        exit(1) # Exit the thread.
        
    return response.text


def initialize():
    global POST_OFFICE
    
    # Initialize messaging
    POST_OFFICE = initialize_apprise( str(__name__) )
    
    # Initialize database
    sql3.initialize_db({
        "Posts" : queries.create_bloggerposts_table,
    })


def main():
    xml_text   = get_xml()
    root       = ET.fromstring(xml_text)
    namespaces = {
        "gd"         : "http://schemas.google.com/g/2005",
        "thr"        : "http://purl.org/syndication/thread/1.0",
        "atom"       : "http://www.w3.org/2005/Atom",
        "openSearch" : "http://a9.com/-/spec/opensearchrss/1.0/",
    }
    
    
    for entry in root.findall("atom:entry", namespaces):
        title     = entry.findtext("atom:title",     namespaces=namespaces)
        published = entry.findtext("atom:published", namespaces=namespaces)
        content   = entry.findtext("atom:content",   namespaces=namespaces)
        
        raw_entry = ET.tostring(entry, encoding="unicode")
        
        store( title, published, content, raw_entry )
        
        
if __name__ == "__main__":
    initialize()
    
    # Start the main loop.
    while 1:
        main()
        print(f"[{__name__}] loop done. sleeping for {INTERVAL}s")
        time.sleep( INTERVAL )
    