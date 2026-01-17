"""
tfj run stats1 --image python3.10 --command "$HOME/local/bin/python3 ~/pybot/editor_stats/src/start.py"

"""
import os
from src.config import editors_dump_path
from src.qids import get_qids_list
from src.sitelinks import load_sitelink_data
from src.by_site import work_in_all_sites
from src.all2 import get_all_editors, work_all_editors


def start():
    qids_list = get_qids_list()
    print(f"len qids_list: {len(qids_list)}")

    sitelinks = load_sitelink_data(qids_list)
    print(f"len sitelinks: {len(sitelinks)}")

    work_in_all_sites()
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
