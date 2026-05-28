import os, dotenv, apprise

#
#   Initialization
#
def initialize_apprise( name : str = None ):
    dotenv.load_dotenv()
    
    discord_webhook = os.getenv( "DISCORD" )
    
    discord_webhook_tail      = discord_webhook.split( "/" )[ -2: ]
    discord_id, discord_token = discord_webhook_tail[ 0 ], discord_webhook_tail[ 1 ]
    
    notifier = apprise.Apprise()
    notifier.add( f"discord://{discord_id}/{discord_token}" )
    
    notifier.notify(
        body=f"-# This is a debug notification that a scraper { '' if name == None else '`' + name + '`' } has been activated.",
    )
    
    return notifier
