import time, threading

import alias
import blogger
import git_actions


from database import main as sql3
from database import queries 

INTERVAL = 60


def blogger_loop():
    while 1:
        blogger.main()
        
        print(f"[{blogger.__name__}] loop done. sleeping for {INTERVAL}s")
        time.sleep( INTERVAL )


def main():    
    # Initialize everything
    alias.initialize()
    blogger.initialize()
    git_actions.initialize()
    
    
    blogger_thread = threading.Thread( target=blogger_loop )
    blogger_thread.start()
    
    while 1:
        
        
        # Search known git instances for known aliases.
        alias.main()
        
        # If any of the tried aliases have a user page, fetch them..
        existing_profiles = sql3.query_database(
            queries.select_200_codes
        )
        
        # .. and try to get their recent activity.
        existing_profile_urls = [ tupl[0] for tupl in existing_profiles ]
        for profile_url in existing_profile_urls:
            git_actions.get_projects( profile_url )
            
        print(f"[{__name__}] loop done. sleeping for {INTERVAL}s")
        time.sleep( INTERVAL )
        
        
if __name__ == "__main__":
    main()