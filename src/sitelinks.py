"""
"""
# ---
import json
import logging

from tqdm import tqdm
from .wiki import wikidataapi_post
from .config import sites_path
from .qids import load_qids_from_file

logger = logging.getLogger(__name__)


def get_sitelinks(qs_list, lena=300):
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
    all_entities = {}
    # ---
    groups = range(0, len(qs_list), lena)
    # ---
    for i in tqdm(groups, desc="get sitelinks from wikidata"):
        # ---
        qids = qs_list[i : i + lena]
        # ---
        params_wd["ids"] = "|".join(qids)
        # ---
        logger.info(f"<<green>> done:{len(all_entities)} from {len(qs_list)}, get sitelinks for {len(qids)} qids.")
        # ---
        json1 = wikidataapi_post(params_wd)
        # ---
        if json1:
            # ---
            entities = json1.get("entities", {})
            # ---
            all_entities = {**all_entities, **entities}
    # ---
    sitelinks = {}
    # ---
    for _qid_1, kk in all_entities.items():
        # ---
        # "abwiki": {"site": "abwiki","title": "Обама, Барак","badges": []}
        # ---
        for _, tab in kk.get("sitelinks", {}).items():
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


def save_sitelink_data(sitelink_data):
    logger.info(f"save_sitelink_data to {sites_path}, len sites: {len(sitelink_data)}")

    if not sitelink_data:
        logger.info("<<red>> no sitelink data to save_sitelink_data")
        return
    # ---
    for site, links in tqdm(sitelink_data.items(), desc="dump sitelink data"):
        # ---
        if not links:
            logger.info(f"<<red>> no links for {site}")
            continue
        # ---
        with open(sites_path / f"{site}.json", "w", encoding="utf-8") as f:
            json.dump(links, f, sort_keys=True)
            logger.info(f"dump <<green>> {site} of {len(links)}")


def load_sitelink_data(qids_list) -> dict:
    # ---
    sitelink_data = get_sitelinks(qids_list, lena=500)
    # ---
    # dump each site to file
    save_sitelink_data(sitelink_data)
    # ---
    return sitelink_data


def start():
    qids_list = load_qids_from_file()
    load_sitelink_data(qids_list)


if __name__ == "__main__":
    start()
