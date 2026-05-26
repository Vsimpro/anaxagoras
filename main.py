import time, requests, argparse
import xml.etree.ElementTree as ET

from git     import Repo
from pathlib import Path

from database import main as sql3
from database import queries


INTERVAL = 60
WEBHOOK  = ""
CLONE    = None 


def notify( link, title, updated ):
    #
    # I opted for Discord, 
    # but if you'd like to use another channel
    # simply modify this function.
    #
    global WEBHOOK
    
    msg = f"""    
# ACTIVITY DETECTED 
`NightmareEclipse` GitLab account has pushed a new repository.  

Repository: [{ link.split('/')[ - 1] }]({ link })
Title: `{ title }`
Timestamp: `{ updated }`
    """
    print(msg)

    response = requests.post(WEBHOOK, json={"content": msg})
    response.raise_for_status()
    

def store(id, link, title, updated, author, raw_entry):
    global CLONE
    
    # Check if repository exists
    exists : int = sql3.query_database( 
        queries.select_title_exists,
        (title,)
    )[ 0 ][ 0 ]
    
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
    local_repo_path = "/".join(link.split("/")[ -2: ])
    if not CLONE:
        return

    if (Path(local_repo_path)).exists():
        return
        
    Repo.clone_from(link, local_repo_path)


def parse_xml( xml : str ):
    root      = ET.fromstring( xml )
    namespace = {
        "atom":  "http://www.w3.org/2005/Atom",
        "media": "http://search.yahoo.com/mrss/",
    }

    # Find and parse the "Entries". One entry is one repository.
    for entry in root.findall("atom:entry", namespace):
        id      = entry.findtext("atom:id",      namespaces=namespace)
        title   = entry.findtext("atom:title",   namespaces=namespace)
        updated = entry.findtext("atom:updated", namespaces=namespace)
        
        link    = entry.find("atom:link",    namespaces=namespace).get("href")
        author  = entry.findtext("atom:author/atom:username",  namespaces=namespace)

        raw_entry = ET.tostring(entry, encoding="unicode")
        
        store(id, link, title, updated, author, raw_entry)


def get_projects( username : str = "nightmare-eclipse" ):
    
    # We can follow the .atom XML of the user.
    url = f"https://gitlab.com/{ username }.atom"
    xml = requests.get( url ).text

    parse_xml( xml )
    

#
#   Main loop.
#
def main():
    global INTERVAL
    
    while 1:    
        get_projects()    
        time.sleep( INTERVAL )
    
    
    
if __name__ == "__main__":
    # Prepare the database
    sql3.initialize_db({
        "Entries" : queries.create_entries_table
    })
    
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--clone",
        action = "store_true",
        help   = "Clone the repositories locally."
    )
    
    parser.add_argument(
        "-w", "--webhook",
        required= True,
        help    = "Discord webhook URL."
    )
    
    args    = parser.parse_args()
    CLONE   = args.clone
    WEBHOOK = args.webhook 
    
    # -> main loop
    main()
    