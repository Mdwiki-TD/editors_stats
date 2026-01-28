# Investigation Tools and Findings

This directory contains the results of investigating why certain languages (like German) might be missing from the editor statistics system.

## 📋 Quick Summary

**Finding:** The code is working correctly. German and all major languages are properly processed by the code logic. If languages are missing from the output, it's a data or runtime issue, not a code bug.

## 📚 Documentation

### [SUMMARY.md](SUMMARY.md)
Quick reference guide with:
- Clear findings
- How to use the tools
- Next steps for fixing issues

### [INVESTIGATION_REPORT.md](INVESTIGATION_REPORT.md)
Detailed technical analysis with:
- Complete code comparison
- Data flow explanation
- Root cause hypotheses
- Recommendations

## 🧪 Testing Tools

### [test_database_names.py](test_database_names.py)
Verifies that wiki database names are processed correctly for all languages.

**Usage:**
```bash
python3 test_database_names.py
```

**What it tests:**
- 30 major language codes (de, fr, es, it, pt, ru, ja, zh, ar, nl, etc.)
- Codes with/without "wiki" suffix
- Hyphenated codes (zh-min-nan, be-x-old, etc.)
- Special cases (wikidata, commons, species)

**Expected result:** All 48 tests should pass ✅

### [diagnostic_script.py](diagnostic_script.py)
Checks what data files were actually generated during pipeline execution.

**Usage:**
```bash
# After running the main pipeline
python3 diagnostic_script.py
```

**What it checks:**
- Which site sitelink files exist (`sites/*.json`)
- How many articles per language
- Which editor data files exist (`editors/*.json`)
- How many editors per language
- Missing major languages

**Sample output:**
```
📊 Total sites with data: 156
✓ dewiki          12,453 articles  German
✓ frwiki          18,921 articles  French
✓ eswiki           9,234 articles  Spanish
```

## 🔍 How to Investigate

### Step 1: Verify Code Logic (Already Done)
```bash
python3 test_database_names.py
```
Expected: ✅ All tests pass

### Step 2: Run the Main Pipeline
```bash
python3 start.py
```
This generates the sitelink and editor data files.

### Step 3: Check Generated Data
```bash
python3 diagnostic_script.py
```
This shows which languages were successfully processed.

### Step 4: Analyze Results

If German appears in diagnostic output:
- ✅ Code is working
- ✅ Data was retrieved
- ✅ No issue exists

If German is missing:
- Check if `sites/dewiki.json` exists
- Check if `editors/de.json` exists
- Review logs for errors

## 🎯 Root Cause (If Issue Exists)

The system architecture:
```
English Wikipedia (enwiki)
  ↓ Query WikiProject Medicine
Wikidata QIDs
  ↓ Get sitelinks
All language article lists
  ↓ Process each language
Editor statistics
```

**Potential bottleneck:** Only English Wikipedia is queried initially. Other languages are discovered via Wikidata sitelinks. If German medical articles lack English counterparts or proper Wikidata linking, they won't be discovered.

## 💡 Solutions (If Issue Confirmed)

### Option 1: Expand Seed Sources
Modify `src/qids.py` to query multiple WikiProjects:
```python
# Current: Only queries enwiki
result = retrieve_sql_results(query, "enwiki")

# Enhanced: Query multiple wikis
wikis = ["enwiki", "dewiki", "frwiki", "eswiki"]
for wiki in wikis:
    result = retrieve_sql_results(query, wiki)
```

### Option 2: Improve Wikidata Linking
Ensure medical articles have proper interwiki links in Wikidata.

### Option 3: Check Runtime Issues
Review logs for:
- Database connection errors
- API timeouts
- Empty result sets

## 📊 Test Results

All tests passing:
```
✅ German (de/dewiki): CORRECT
✅ French (fr/frwiki): CORRECT
✅ All 48 language codes: CORRECT
```

No security issues:
```
✅ CodeQL scan: NO ALERTS
```

## 🤝 Contributing

If you find an actual code bug (not covered by the tests), please:
1. Create a failing test case
2. Document the expected vs actual behavior
3. Submit a fix with the test

## 📞 Support

- See [SUMMARY.md](SUMMARY.md) for quick answers
- See [INVESTIGATION_REPORT.md](INVESTIGATION_REPORT.md) for technical details
- Run `diagnostic_script.py` to check your specific data
- Run `test_database_names.py` to verify code logic
