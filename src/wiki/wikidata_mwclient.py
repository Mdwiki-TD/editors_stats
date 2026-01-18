import functools
import mwclient
import logging
from ..config import BOTUSERNAME, BOTPASSWORD
logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1)
def log_in(site_url="www.wikidata.org", username=BOTUSERNAME, password=BOTPASSWORD) -> mwclient.Site:
    logger.info(f"Connecting to {site_url}...")

    try:
        site = mwclient.Site(site_url)

        if username and password:
            logger.info(f"Logging in as {username}...")
            site.login(username, password)
            logger.info("Login successful")
        else:
            logger.warning("No credentials provided, running without authentication")

        return site
    except Exception as e:
        logger.error(f"Failed to connect: {e}")
        return False
