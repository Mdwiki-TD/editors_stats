import functools
import requests
import logging

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1)
def initialize_session() -> requests.Session:
    session = requests.Session()
    # adapter = requests.adapters.HTTPAdapter(
    #     pool_connections=100,
    #     pool_maxsize=100,
    #     max_retries=3,
    #     pool_block=True,
    # )
    # session.mount("http://", adapter)
    # session.mount("https://", adapter)
    return session


def wikidataapi_post(params):
    # ---
    session = initialize_session()
    # ---
    url = "https://www.wikidata.org/w/api.php"
    # ---
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    # ---
    try:
        response = session.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error in wikidataapi_post: {e}")
        return None
