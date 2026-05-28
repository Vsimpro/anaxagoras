import xml.etree.ElementTree as ET
from urllib.parse import urlparse




#
#   Interface.
#
def parse_xml( url, xml ):
    global GIT_INSTANCES
    
    git_instance = instance_name( url )
    if git_instance not in GIT_INSTANCES:
        print(f"[{__name__}] Git Instance {git_instance} is not yet supported.") 
        return
    
    if GIT_INSTANCES[ git_instance ] == None:
        print(f"[{__name__}] Git Instance {git_instance} is not yet supported.")
        return
    
    return GIT_INSTANCES[ git_instance ]( xml )


#
#   Implementation 
#
def instance_name( url ):
    if "://" not in url:
        url = "http://" + url
    
    return urlparse(url).netloc


def normalize_repo_link(link: str) -> str:
    parsed = urlparse(link)
    parts  = [p for p in parsed.path.split("/") if p]
    
    if len(parts) >= 2:
        return f"{parsed.scheme}://{parsed.netloc}/{parts[0]}/{parts[1]}"
    
    return link


def parse_generic_xml( xml : str ):
    root      = ET.fromstring( xml )
    namespace = {
        "atom":  "http://www.w3.org/2005/Atom",
        "media": "http://search.yahoo.com/mrss/",
    }
    
    # TODO: Error tracking for empty entries.
    no_entries = True
    
    # Find and parse the "Entries". One entry is one repository.
    for entry in root.findall("atom:entry", namespace):
    
        no_entries = False
    
        id      = entry.findtext("atom:id",      namespaces=namespace)
        title   = entry.findtext("atom:title",   namespaces=namespace)
        updated = entry.findtext("atom:updated", namespaces=namespace)
        
        link_t  = entry.find("atom:link[@rel='alternate']", namespaces=namespace)
        if link_t is None:
            link_t = entry.find("atom:link", namespaces=namespace)
        
        if link_t is None:
            continue
        
        link = link_t.get("href")
        link = normalize_repo_link(link)
        
        author = entry.findtext("atom:author/atom:username", namespaces=namespace)
        if author is None:
            author = entry.findtext("atom:author/atom:name", namespaces=namespace)
        
        raw_entry = ET.tostring(entry, encoding="unicode")
    
    return id, link, title, updated, author, raw_entry


GIT_INSTANCES = {
    "github.com"      : parse_generic_xml,
    "gitlab.com"      : parse_generic_xml,
    "codeberg.org"    : parse_generic_xml,
    "gitee.com"       : None,
    "gitflic.ru"      : None,
    "framagit.org"    : parse_generic_xml,
    "git.disroot.org" : parse_generic_xml,
    "tildegit.org"    : parse_generic_xml,
}
