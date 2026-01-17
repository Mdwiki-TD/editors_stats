"""
"""
import json
import os

from .api_sql import retrieve_sql_results
from .config import main_dump_path

qids_file = main_dump_path / "qids.json"

if not os.path.exists(qids_file):
    with open(qids_file, "w", encoding="utf-8") as f:
        json.dump({}, f, sort_keys=True)


def load_qids_from_file():
    qids_list = {}

    with open(qids_file, "r", encoding="utf-8") as f:
        qids_list = json.load(f)
    return qids_list


def get_en_articles():
    # ---
    query = """
    SELECT p.page_title, pp_value
        FROM page p, categorylinks, page_props, page p2
        WHERE p.page_id = cl_from
        AND cl_to = 'All_WikiProject_Medicine_pages'
        # AND cl_to = 'All_WikiProject_Medicine_articles'
        AND p.page_namespace = 1
        AND p2.page_namespace = 0
        AND pp_propname = 'wikibase_item'
        and p.page_title = p2.page_title
        and pp_page = p2.page_id
    """
    # ---
    result = retrieve_sql_results(query, "enwiki")
    return {x["page_title"]: x["pp_value"] for x in result}


def get_qids_list():
    # ---
    articles = get_en_articles()
    # ---
    print(f"len articles: {len(articles)}")
    # ---
    qids_list = list(articles.values())
    # ---
    with open(qids_file, "w", encoding="utf-8") as f:
        json.dump(qids_list, f, sort_keys=True)

    print(f"dumped {len(qids_list)} qids to {qids_file}")

    return qids_list
