"""
tfj run stats --image python3.9 --command "$HOME/local/bin/python3 ~/pybot/editor_stats/start.py"

"""
import os

from src.all2 import get_all_editors, work_all_editors
from src.by_site import get_files_sorted_by_size, work_in_one_site, extract_site_editors
from src.config import editors_dump_path
from src.qids import get_qids_list
from src.sitelinks import load_sitelink_data


def start():
    qids_list = get_qids_list()
    print(f"len qids_list: {len(qids_list)}")

    sitelinks = load_sitelink_data(qids_list)
    print(f"len sitelinks: {len(sitelinks)}")

    # read json files in sites_path
    files = get_files_sorted_by_size()
    # ---
    for numb, (site_code, links) in enumerate(files.items(), start=1):
        # ---
        print(f"<<green>> n: {numb} site_code: {site_code}:")
        # ---
        editors = extract_site_editors(site_code, links)
        # ---
        if not editors:
            print("<<red>> no editors")
            continue
        # ---
        work_in_one_site(site_code, links, editors)

    # ---
    files = os.listdir(editors_dump_path)
    print(f"len files: {len(files)}")
    # ---
    all_editors = get_all_editors(files)
    print(f"len all_editors: {len(all_editors)}")
    # ---
    work_all_editors(all_editors)


if __name__ == "__main__":
    start()
