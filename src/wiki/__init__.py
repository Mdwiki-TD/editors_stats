

from .wikidata import wikidataapi_post
from .mdwiki_page_mwclient import page_mwclient as page
from .wikidata_mwclient import log_in

__all__ = [
    "page",
    "wikidataapi_post",
    "log_in",
]
