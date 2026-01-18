"""
tfj run stats --image python3.9 --command "$HOME/local/bin/python3 ~/pybot/editor_stats/start.py"

"""
import os
import sys
import logging

from src.all2 import get_all_editors, work_all_editors
from src.by_site import get_files_sorted_by_size, work_in_one_site, extract_site_editors
from src.config import editors_dump_path, MAIN_PATH
from src.qids import get_qids_list
from src.sitelinks import load_sitelink_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(MAIN_PATH / 'remove_red_categories.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# logger.setLevel(logging.INFO)


def start():
    qids_list = get_qids_list()
    logger.info(f"len qids_list: {len(qids_list)}")

    sitelinks = load_sitelink_data(qids_list)
    logger.info(f"len sitelinks: {len(sitelinks)}")

    # read json files in sites_path
    files = get_files_sorted_by_size()
    # ---
    for numb, (site_code, links) in enumerate(files.items(), start=1):
        # ---
        logger.info(f"<<green>> n: {numb} site_code: {site_code}:")
        # ---
        editors = extract_site_editors(site_code, links)
        # ---
        if not editors:
            logger.info("<<red>> no editors")
            continue
        # ---
        work_in_one_site(site_code, links, editors)

    # ---
    files = os.listdir(editors_dump_path)
    logger.info(f"len files: {len(files)}")
    # ---
    all_editors = get_all_editors(files)
    logger.info(f"len all_editors: {len(all_editors)}")
    # ---
    work_all_editors(all_editors)


if __name__ == "__main__":
    start()
