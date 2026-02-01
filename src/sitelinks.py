"""
"""
# ---
import json
import logging

from tqdm import tqdm
from .wiki import wikidataapi_post, log_in
from .config import BOTUSERNAME, BOTPASSWORD, sites_path, qids_sitelinks_path
from .qids import load_qids_from_file

logger = logging.getLogger(__name__)


def wikidata_mwclient_post(params):
    # ---
    site = log_in(site_url="www.wikidata.org", username=BOTUSERNAME, password=BOTPASSWORD)
    # ---
    params.pop("action", None)  # remove action from params as mwclient api method uses action internally
    # ---
    try:
        # response = site.api(params)
        response = site.api('wbgetentities', **params)
        return response
    except Exception as e:
        logger.error(f"Error in wikidata_mwclient_post: {e}")
        return None


def wrap_post(params):
    if BOTUSERNAME and BOTPASSWORD:
        return wikidata_mwclient_post(params)
    return wikidataapi_post(params)


def save_one_qid_sitelinks(qid, sitelinks):
    if not sitelinks:
        logger.error(f"<<red>> no sitelinks for {qid} to save")
        return

    with open(qids_sitelinks_path / f"{qid}.json", "w", encoding="utf-8") as f:
        json.dump(sitelinks, f, sort_keys=True)

    # logger.info(f"dumped sitelinks for {qid} to {qids_sitelinks_path / f'{qid}.json'}")


def get_sitelinks(qs_list, lena=50):
    # ---
    qs_list = list(qs_list)
    # ---
    params_wd = {
        "action": "wbgetentities",
        "format": "json",
        # "ids": ,
        "redirects": "yes",
        "props": "sitelinks",
        "utf8": 1,
    }
    # ---
    all_entities = 0
    sitelinks = {}
    # ---
    groups = range(0, len(qs_list), lena)
    # ---
    for i in tqdm(groups, desc="get sitelinks from wikidata"):
        # ---
        qids = qs_list[i : i + lena]
        # ---
        params_wd["ids"] = "|".join(qids)
        # ---
        logger.info(f"<<green>> done:{all_entities:,} from {len(qs_list)}, get sitelinks for {len(qids)} qids.")
        # ---
        json1 = wrap_post(params_wd)
        # ---
        if not json1:
            logger.info("<<red>> no json1 from wrap_post")
            continue
        # ---
        entities = json1.get("entities", {})
        # ---
        if not entities:
            logger.info("<<red>> no entities in json1")
            logger.error(json1)
            continue
        # ---
        # { "entities": { "Q805": { "type": "item", "id": "Q805", "sitelinks": { "abwiki": { "site": "abwiki", "title": "Иемен", "badges": [] }, "acewiki": { "site": "acewiki", "title": "Yaman", "badges": [] },
        # ---
        all_entities += len(entities)
        # ---
        for qid, data in entities.items():
            # ---
            qid_sitelinks = data.get("sitelinks", {})
            # ---
            save_one_qid_sitelinks(qid, qid_sitelinks)
            # ---
            # "abwiki": {"site": "abwiki","title": "Обама, Барак","badges": []}
            # ---
            for _, tab in qid_sitelinks.items():
                # ---
                title = tab.get("title", "")
                site = tab.get("site", "")
                # ---
                if site not in sitelinks:
                    sitelinks[site] = []
                # ---
                sitelinks[site].append(title)
    # ---
    return sitelinks


def load_qid_sitelinks(qid) -> dict:
    if not qid:
        logger.error(f"<<red>> invalid qid: {qid}")
        return {}

    file_path = qids_sitelinks_path / f"{qid}.json"
    if not file_path.exists():
        logger.error(f"<<red>> sitelink file does not exist for {qid}")
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            qid_sitelinks = json.load(f)
            return qid_sitelinks
    except FileNotFoundError:
        logger.error(f"<<red>> sitelink file not found for {qid}")
        return {}


def check_qid_sitelinks(qid) -> bool:
    file_path = qids_sitelinks_path / f"{qid}.json"
    if not file_path.exists():
        logger.error(f"<<red>> sitelink file does not exist for {qid}")
        return False
    return True


def save_sitelink_data(sitelink_data):
    logger.info(f"save_sitelink_data to {sites_path}, len sites: {len(sitelink_data)}")

    if not sitelink_data:
        logger.info("<<red>> no sitelink data to save_sitelink_data")
        return
    # ---
    for site, links in tqdm(sitelink_data.items(), desc="dump sitelink data"):
        # ---
        if not links:
            logger.error(f"<<red>> no links for {site}")
            continue
        # ---
        with open(sites_path / f"{site}.json", "w", encoding="utf-8") as f:
            json.dump(links, f, sort_keys=True)
            logger.info(f"dump <<green>> {site} of {len(links)}")


def load_sitelink_data_online(qids_list) -> dict:
    # ---
    sitelink_data = get_sitelinks(qids_list, lena=500)
    # ---
    # dump each site to file
    save_sitelink_data(sitelink_data)
    # ---
    return sitelink_data


def load_sitelink_data(qids_list) -> None:
    to_load = []
    # ---
    for qid in tqdm(qids_list, desc="load sitelink data from files"):
        if not check_qid_sitelinks(qid):
            to_load.append(qid)
    # ---
    if to_load:
        logger.info(f"<<yellow>> need to load sitelinks online for {len(to_load)} qids")
        sitelink_data_online = load_sitelink_data_online(to_load)
        logger.info(f"<<green>> loaded sitelink data online, sitelink_data_online len: {len(sitelink_data_online)}")


def start():
    qids_list = load_qids_from_file()
    load_sitelink_data(qids_list)


if __name__ == "__main__":
    start()
