"""

python3 core8/pwb.py stats/by_site
tfj run stats2 --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py stats/by_site"

"""
import json
import re
import logging
import os
import sys
from datetime import datetime
from .wiki import page
from .editors import get_editors, validate_ip
from .config import sites_path

logger = logging.getLogger(__name__)
last_year = datetime.now().year - 1
skip_sites = ["enwiki", "wikidatawiki", "commonswiki", "specieswiki"]


def filter_editors(editors, site):
    # ---
    editors = dict(sorted(editors.items(), key=lambda x: x[1], reverse=True))
    # ---
    for x, v in editors.copy().items():
        if validate_ip(x):
            del editors[x]
    # ---
    # del editor with less then 100 edits
    for x, v in editors.copy().items():
        if v < 10:
            del editors[x]
    # ---
    # del Mr. Ibrahem if site != 'arwiki'
    if site != "ar":
        if "Mr._Ibrahem" in editors:
            del editors["Mr._Ibrahem"]
        if "Mr. Ibrahem" in editors:
            del editors["Mr. Ibrahem"]
    # ---
    return editors


def work_in_one_site(site, links):
    # ---
    site = re.sub(r"wiki$", "", site)
    # ---
    logger.info(f"<<green>> site:{site} links: {len(links)}")
    # ---
    if len(links) < 100:
        logger.info("<<red>> less than 100 articles")
        # return
    # ---
    editors = get_editors(links, site)
    # ---
    editors = filter_editors(editors, site)
    # ---
    if not editors:
        logger.info("<<red>> no editors")
        return
    # ---
    if "dump" in sys.argv:
        print("json.dumps(editors, indent=2)")
        return
    # ---
    title = f"WikiProjectMed:WikiProject_Medicine/Stats/Top_medical_editors_{last_year}/{site}"
    # ---
    text = "{{:WPM:WikiProject Medicine/Total medical articles}}\n"
    text += f"{{{{Top medical editors by lang|{last_year}}}}}\n"
    # ---
    if site != "ar":
        text += f"Numbers of {last_year}. There are {len(links):,} articles in {site}\n"
    # ---
    text += """{| class="sortable wikitable"\n!#\n!User\n!Count\n|-"""
    # ---
    for i, (user, count) in enumerate(editors.items(), start=1):
        # ---
        user = user.replace("_", " ")
        # ---
        text += f"\n|-\n!{i}\n|[[:w:{site}:user:{user}|{user}]]\n|{count:,}"
        # ---
        if i == 100:
            break
        # ---
    # ---
    text += "\n|}"
    # ---
    page_obj = page(title, "www", family="mdwiki")
    p_text = page_obj.get_text()
    # ---
    if p_text != text:
        page_obj.save(newtext=text, summary="update", nocreate=0, minor="")
    else:
        logger.info("<<green>> no changes")
    # ---
    return editors


def work_in_all_sites(p_site="") -> None:
    # ---
    # read json files in sites_path
    files = os.listdir(sites_path)
    # ---
    # sort files by biggest size
    files = sorted(files, key=lambda x: os.stat(sites_path / x).st_size, reverse=True)
    # ---
    for numb, file in enumerate(files, start=1):
        # ---
        logger.info(f"<<green>> n: {numb} file: {file}:")
        # ---
        if not file.endswith("wiki.json"):
            continue
        # ---
        site = file[:-5]
        # ---
        if site in skip_sites:
            continue
        # ---
        if p_site and f"{p_site}wiki" != site:
            continue
        # ---
        with open(sites_path / file, "r", encoding="utf-8") as f:
            links = json.load(f)
        # ---
        work_in_one_site(site, links)


def start():
    # ---
    p_site = ""
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "site":
            p_site = value
    # ---
    work_in_all_sites(p_site)


if __name__ == "__main__":
    start()
