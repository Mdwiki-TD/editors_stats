"""

"""
from ..api_sql import retrieve_sql_results

from datetime import datetime

last_year = datetime.now().year - 1


def get_ar_results():
    qua = f"""
    SELECT actor_name, count(*) as count from revision
        join actor on rev_actor = actor_id
        join page on rev_page = page_id
        WHERE lower(cast(actor_name as CHAR)) NOT LIKE '%bot%' AND page_namespace = 0 AND rev_timestamp like '{last_year}%'
        and page_id in (
        select DISTINCT pa_page_id
        from page_assessments, page_assessments_projects
        where pa_project_id = pap_project_id
        and pap_project_title = "طب"
        )
        group by actor_id
        order by count(*) desc
    limit 100;
    """
    # ---
    editors = {}
    # ---
    result = retrieve_sql_results(qua, "arwiki")
    # ---
    for x in result:
        # ---
        actor_name = x["actor_name"]
        # ---
        if actor_name not in editors:
            editors[actor_name] = 0
        # ---
        editors[actor_name] += x["count"]
        # ---
    # ---
    return editors
