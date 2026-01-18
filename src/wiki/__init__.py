

from .wikidata import wikidataapi_post
from .mdwiki_page_mwclient import page_mwclient as page

__all__ = [
    "page",
    "wikidataapi_post",
]
