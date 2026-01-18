"""

"""
# ---
import functools
import logging

import mwclient

from ..config import mdwiki_pass, my_username

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1)
def initialize_site_connection(username, password):
    site_mw = mwclient.Site("www.mdwiki.org")
    try:
        site_mw.login(username, password)

    except mwclient.errors.LoginError as e:
        logger.error(f"Error logging in: {e}")
    return site_mw


class page_mwclient:
    def __init__(self, title: str):
        self.title = title
        self.username = my_username
        self.password = mdwiki_pass

        self.site_mw = initialize_site_connection(self.username, self.password)

        self.page = self.site_mw.pages[title]

    def get_text(self):
        return self.page.text()

    def exists(self):
        return self.page.exists

    def save(self, newtext: str, summary: str):
        result = self.page.save(newtext, summary=summary)
        logger.info(f"Saved page {self.title} with result: {result}")
        return result

    def create(self, newtext: str, summary: str):
        result = self.page.save(newtext, summary=summary)
        logger.info(f"Created page {self.title} with result: {result}")
        return result
