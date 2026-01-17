"""

"""
import json
import re
import os
import sys
from pymysql.converters import escape_string
from datetime import datetime
import tqdm

from config import editors_dump_path

from .utils.ar import get_ar_results
from .api_sql import retrieve_sql_results

last_year = datetime.now().year - 1


def validate_ip(ip_address):
    if ip_address == "CommonsDelinker":
        return True
    # IPv4 pattern
    ipv4_pattern = r"^\b(?:\d{1,3}\.){3}\d{1,3}\b$"
    # IPv6 pattern
    ipv6_pattern = r"^\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b$"

    if re.match(ipv4_pattern, ip_address):
        return True
    elif re.match(ipv6_pattern, ip_address):
        return True
    return False


def get_editors_sql(links, site, split_by=100):
    # ---
    qua = f"""
        SELECT actor_name, count(*) as count from revision
            join actor on rev_actor = actor_id
            join page on rev_page = page_id
            WHERE lower(cast(actor_name as CHAR)) NOT LIKE '%bot%' AND page_namespace = 0 AND rev_timestamp like '{last_year}%'
            and page_id in (
            select page_id
            from page
                where page_title in (
                    %s
                )
            )
        group by actor_id
        order by count(*) desc
    """
    # ---
    editors = {}
    # ---
    for i in tqdm.tqdm(range(0, len(links), split_by), desc=f"get_editors_sql site:{site}", total=len(links) // split_by):
        # ---
        pages = links[i : i + split_by]
        # ---
        # lim = ' , '.join(['?' for x in pages])
        lim = ",".join([f'"{escape_string(x)}"' for x in pages])
        # ---
        qua2 = qua.replace("%s", lim)
        # ---
        # print(qua2)
        # ---
        edits = retrieve_sql_results(qua2, site)
        # ---
        for x in edits:
            # ---
            actor_name = x["actor_name"]
            # ---
            # skip if actor_name iis IP address
            if validate_ip(actor_name):
                continue
            # ---
            if actor_name not in editors:
                editors[actor_name] = 0
            # ---
            editors[actor_name] += x["count"]
            # ---
        # ---
    return editors


def dumpit(editors, site):
    with open(editors_dump_path / f"{site}.json", "w", encoding="utf-8") as f:
        json.dump(editors, f, sort_keys=True)


def get_editors(links, site, do_dump=True):
    editors = {}
    # ---
    if os.path.exists(editors_dump_path / f"{site}.json"):
        with open(editors_dump_path / f"{site}.json", "r", encoding="utf-8") as f:
            editors = json.load(f)
            return editors
    # ---
    if site == "ar":
        editors = get_ar_results()
    else:
        editors = get_editors_sql(links, site, split_by=150)
    # ---
    if ("dump" in sys.argv or do_dump) and editors:
        dumpit(editors, site)
        return editors
    # ---
    return editors
