import os, time, dotenv, apprise, requests

from src.msg_relay import initialize_apprise

from database import main as sql3
from database import queries 


# Global Variables
POST_OFFICE = None
INTERVAL    = 60

#
#   Notifier
#
def notify( url, status_code, old_code):
    global POST_OFFICE
    
    POST_OFFICE.notify(
        title = "## Change detected!",
        body  = f"`{ url }` \n changed from `{ old_code }` --> `{ status_code }`"
    )


#
#   Scraping & Generation
#
def generate_aliases():
    """
    Known aliases: ChaoticEclipse0, nightmare-eclipse, and deadeclipse666. 
    """
    
    aliases : list[str] = []   
     
    for adj in ["chaotic", "nightmare", "dead"]:
        for mid in ["-", ""]:
            for suffix in ["", "0", "666"]:
                aliases.append( adj + mid + "eclipse" + suffix )
                
    return aliases


def generate_urls( base_url_list : list, username_list : list ):

    urls : list[str] = []
    
    for url in base_url_list:
        for username in username_list:
            urls.append( url + username )
            
    return urls


def get_status( url ):
    return requests.head( url ).status_code


def diff_and_save( url, status_code ):
    
    result = sql3.query_database(
        queries.select_status_code,
        (url,)
    )
    
    # First run or new url
    if result == []:
        sql3.insert_data(
            queries.insert_gitprofiles,
            (str(url), int(status_code))
        )
        
        return False 
    
    # Check if site goes down (possible with small git instances)
    if status_code >= 500:
        print(f"[{__name__}] The url { url } is currently experiencing problems: { status_code }. Ignoring.")
        return False
    
    # Diff!
    old_status_code = result[ 0 ][ 0 ]
    if old_status_code != status_code:
        print(f"[{__name__}] Noticed a DIFF in { url }. (Old,New) = {old_status_code,status_code}")
        
        notify( url, status_code, old_status_code )
        
        sql3.update_data(
            queries.update_status_code_gitprofiles,
            (status_code, url)
        )
        
        return True

    return False


def initialize():
    global POST_OFFICE
    
    # Initialize messaging
    POST_OFFICE = initialize_apprise( str(__name__) )
    
    # Initialize database
    sql3.initialize_db({
        "GitProfiles" : queries.create_gitprofiles_table
    })
    

#
#   Main loop
#
def main():
    
    alias_list = generate_aliases()
    git_list   = [
        "https://github.com/", # yes I know their account is banned. But it might reappear.
        "https://gitlab.com/",
        "https://codeberg.org/",
        "https://gitee.com/",
        "https://gitflic.ru/user/",
        "https://framagit.org/",
        "https://git.disroot.org/",
        "https://tildegit.org/",
        "https://sr.ht/~",
        "https://gitea.com/",
        "https://foss.heptapod.net/",
        "https://0xacab.org/",
    ]
    
    # Iterate through all the services
    for url in generate_urls( git_list, alias_list ):
        status = get_status( url )
        diff_and_save(url, status)
        
        print(f"[{__name__}] <{ url }>, status: { status }")
        
    
if __name__ == "__main__":    
    # Start the main loop.
    while 1:
        main()
        print(f"[{__name__}] loop done. sleeping for {INTERVAL}s")
        time.sleep( INTERVAL )
