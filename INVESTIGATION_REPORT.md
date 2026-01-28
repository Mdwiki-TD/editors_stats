# Investigation Report: Missing Languages in Editor Stats

## Executive Summary

After comparing the improved code in this repository with the original code at `https://github.com/Mdwiki-TD/mdwiki-python-files/tree/main/md_core/stats`, I have found that **the code logic is essentially identical** between the two versions. German (dewiki) and other languages should be processed correctly based on the code structure.

## Code Comparison Results

### Files Compared
1. `qids.py` - Identical logic
2. `sitelinks.py` - Identical logic  
3. `editors.py` - Identical logic
4. `by_site.py` - Identical logic
5. `all2.py` - Identical logic
6. `ar.py` - Identical logic

### Key Differences Found
The only substantial differences between old and new code are:

| Old Code | New Code | Impact |
|----------|----------|--------|
| `from mdapi_sql import wiki_sql` | `from .api_sql import retrieve_sql_results` | Reimplemented locally |
| `from apis import wikidataapi` | `from .wiki import wikidataapi_post` | Reimplemented locally |
| `from newapi import printe` | `import logging` | Changed logging approach |
| `from newapi.mdwiki_page import md_MainPage` | `from .wiki import page` | Reimplemented locally |

**All functional logic remains the same.**

## How Language Processing Works

### Data Flow
1. **English Wikipedia Query** (`src/qids.py`)
   - Queries `enwiki` for articles in `All_WikiProject_Medicine_pages` category
   - Extracts Wikidata QIDs (e.g., Q1234567)
   
2. **Wikidata Sitelinks** (`src/sitelinks.py`)
   - Calls Wikidata API with QIDs
   - Gets sitelinks for ALL language versions (including dewiki, frwiki, etc.)
   - Saves each language's article list to separate JSON files
   
3. **Processing Each Wiki** (`src/by_site.py`)
   - Reads JSON files for each language
   - Filters out: `enwiki`, `wikidatawiki`, `commonswiki`, `specieswiki`
   - **German (dewiki) is NOT filtered out**
   - Processes remaining wikis including dewiki

4. **SQL Queries** (`src/editors.py`, `src/api_sql/wiki_sql.py`)
   - For each wiki (e.g., "dewiki")
   - Strips "wiki" suffix → "de"
   - Converts back to proper database name → "dewiki"
   - Queries Wikimedia analytics database at `dewiki.analytics.db.svc.wikimedia.cloud`

### Test Results
```
Input: de       → Output: dewiki (✓ Correct)
Input: dewiki   → Output: dewiki (✓ Correct)
Input: fr       → Output: frwiki (✓ Correct)
Input: ar       → Output: arwiki (✓ Correct)
```

## Root Cause Analysis

The code does NOT explicitly filter out German or any other major languages. The potential issues are:

### Hypothesis 1: Data Dependency (Most Likely)
- The system relies on **English Wikipedia medical articles as the seed**
- German articles only included if they have:
  1. A corresponding English medical article
  2. Proper Wikidata cross-linking
- If German medical articles lack English equivalents, they won't be discovered

### Hypothesis 2: Runtime Execution Issue
- Code logic is correct, but execution might be failing for certain wikis:
  - Database connectivity issues
  - API timeout or rate limiting
  - Insufficient permissions
  - Empty sitelink data from Wikidata

### Hypothesis 3: Data Volume Threshold
- Line 52 in `by_site.py`: Logs warning if < 100 articles (but doesn't skip)
- If German medical articles linked from English are < 100, might be logged as problematic

## Recommendations

### To Confirm the Issue:
1. **Check Sitelink Data**: Examine the generated JSON files in the `sites/` directory
   - Does `dewiki.json` exist?
   - How many articles does it contain?
   
2. **Check Editor Data**: Examine the generated JSON files in the `editors/` directory
   - Does `de.json` exist?
   - Does it contain editor data?

3. **Run with Debug Logging**: Enable debug logging to see:
   - Which wikis are being processed
   - SQL query results for each wiki
   - Any errors during execution

### Potential Solutions:

#### Option 1: Expand Seed Data Sources
Instead of only querying English Wikipedia, also query:
- German WikiProject Medicine (`dewiki`)
- French WikiProject Medicine (`frwiki`)  
- Other major language medical projects

#### Option 2: Verify Wikidata Linking
- Ensure English medical articles have proper Wikidata interwiki links
- Check if German medical articles are properly tagged in Wikidata

#### Option 3: Add Direct Language Queries
Modify `qids.py` to directly query multiple language Wikipedias, not just English

## Conclusion

**The code structure does NOT prevent German from being processed.** The issue is likely:
1. **Data-related**: Not enough German articles are linked to English medical articles via Wikidata
2. **Runtime-related**: Execution errors not visible in the code itself

To diagnose further, we need to:
- Run the code and examine the generated data files
- Check logs for errors or warnings
- Verify Wikidata sitelink coverage for medical articles

The new code is a faithful reimplementation of the old code. If the old code successfully processed German and the new code doesn't, the issue is in the **dependencies** (`mdapi_sql`, `apis`) which we cannot access directly, not in the **logic**.
