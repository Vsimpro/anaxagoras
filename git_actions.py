import requests

from git     import Repo
from pathlib import Path

from src.msg_relay   import initialize_apprise
from src.xml_parsing import parse_xml, instance_name

from database import main as sql3
from database import queries


INTERVAL      = 60
WEBHOOK       = ""
CLONE         = True
HEADERS       = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def notify( link, title, updated ):
    global POST_OFFICE 
    
    repository = link.split('/')[ -1 ]  
    username   = link.split("/")[ -2 ] 
    
    POST_OFFICE.notify(
        title = "# ACTIVITY DETECTED",
        body  = f"Git account `{ username }` has pushed a new repository. \n Repository: [{ repository }]({ link }) \n Title: `{ title }` \n Timestamp: `{ updated }`"
    )


def store(id, link, title, updated, author, raw_entry):
    global CLONE

    conn = sql3.query_database(
            queries.select_title_exists,
            (title,)
    )

    if not conn:
        return
    
    # Check if repository exists
    exists : int = conn[ 0 ][ 0 ]

    # Stored! No need to continue.
    if exists == 1:
        return

    # Send a notification that a new repo has appeared.
    notify( link, title, updated )

    # .. and store the repository.
    sql3.insert_data(
        queries.insert_entries,
        (id, link, title, updated, author, raw_entry)
    )
    
    # .. and clone, just in case of takedowns.
    local_repo_path = instance_name(link) + "/" + "/".join(link.split("/")[ -2: ])
    if not CLONE:
        return

    if (Path(local_repo_path)).exists():
        return

    Repo.clone_from(link, local_repo_path)


def get_projects( git_profile_link ):
    global HEADERS

    # We can follow the .atom XML of the user.
    url = f"{ git_profile_link }.atom"

    try:
        
        # Get the XML and parse it.
        xml = requests.get( url , timeout=(5, 10), headers = HEADERS)
        xml.raise_for_status()
        
        entries = parse_xml( url, xml.text )
        for entry in entries:
            id, link, title, updated, author, raw_entry  = entry
            store(id, link, title, updated, author, raw_entry)
    
    # Bit of a hack. xml_parsing tries to return empty values, 
    # there are no entries. We can catch that here.
    except UnboundLocalError:
        print(f"[{__name__}] UnboundLocalError, meaning no entries yet.")

    # Uncaught and unhandled "not yet supported."
    except TypeError as e:
        print(f"[{__name__}] TypeError, likely a known error: {e}. See above, if there's a mention of the cause.")

    # Some other error.
    except Exception as e:
        print(f"[{__name__}][!] Ran into an exception, {e}")


def initialize():
    global POST_OFFICE
    
    # Initialize messaging
    POST_OFFICE = initialize_apprise( str(__name__) )
    
    # Prepare the database
    sql3.initialize_db({
        "Entries" : queries.create_entries_table
    })
