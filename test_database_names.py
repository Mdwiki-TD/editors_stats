#!/usr/bin/env python3
"""
Test script to verify wiki database name processing for all common languages.

This ensures that the make_labsdb_dbs_p function correctly handles:
1. Regular language codes (de, fr, es, etc.)
2. Hyphenated codes (zh-min-nan, be-x-old, etc.)  
3. Codes with/without "wiki" suffix
4. Special cases that need custom mapping
"""

import sys
from pathlib import Path

# Add parent to path and import correctly
sys.path.insert(0, str(Path(__file__).parent))

from src.api_sql.wiki_sql import make_labsdb_dbs_p


def test_regular_languages():
    """Test common language codes"""
    print("=" * 70)
    print("TESTING REGULAR LANGUAGE CODES")
    print("=" * 70)
    
    regular_langs = [
        ("de", "dewiki_p", "German"),
        ("fr", "frwiki_p", "French"),
        ("es", "eswiki_p", "Spanish"),
        ("it", "itwiki_p", "Italian"),
        ("pt", "ptwiki_p", "Portuguese"),
        ("ru", "ruwiki_p", "Russian"),
        ("ja", "jawiki_p", "Japanese"),
        ("zh", "zhwiki_p", "Chinese"),
        ("ar", "arwiki_p", "Arabic"),
        ("nl", "nlwiki_p", "Dutch"),
        ("pl", "plwiki_p", "Polish"),
        ("sv", "svwiki_p", "Swedish"),
        ("tr", "trwiki_p", "Turkish"),
        ("uk", "ukwiki_p", "Ukrainian"),
        ("vi", "viwiki_p", "Vietnamese"),
        ("cs", "cswiki_p", "Czech"),
        ("fa", "fawiki_p", "Persian"),
        ("id", "idwiki_p", "Indonesian"),
        ("no", "nowiki_p", "Norwegian"),
        ("fi", "fiwiki_p", "Finnish"),
        ("he", "hewiki_p", "Hebrew"),
        ("da", "dawiki_p", "Danish"),
        ("ro", "rowiki_p", "Romanian"),
        ("hu", "huwiki_p", "Hungarian"),
        ("el", "elwiki_p", "Greek"),
        ("th", "thwiki_p", "Thai"),
        ("ca", "cawiki_p", "Catalan"),
        ("sr", "srwiki_p", "Serbian"),
        ("bg", "bgwiki_p", "Bulgarian"),
        ("sk", "skwiki_p", "Slovak"),
    ]
    
    passed = 0
    failed = 0
    
    for input_code, expected_db, lang_name in regular_langs:
        host, db = make_labsdb_dbs_p(input_code)
        
        if db == expected_db:
            print(f"  ✓ {input_code:10} → {db:20} ({lang_name})")
            passed += 1
        else:
            print(f"  ❌ {input_code:10} → {db:20} (expected: {expected_db}) ({lang_name})")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0


def test_with_wiki_suffix():
    """Test that codes with 'wiki' suffix are handled correctly"""
    print("\n" + "=" * 70)
    print("TESTING CODES WITH 'wiki' SUFFIX")
    print("=" * 70)
    
    test_cases = [
        ("dewiki", "dewiki_p", "German"),
        ("frwiki", "frwiki_p", "French"),
        ("enwiki", "enwiki_p", "English"),
        ("arwiki", "arwiki_p", "Arabic"),
    ]
    
    passed = 0
    failed = 0
    
    for input_code, expected_db, lang_name in test_cases:
        host, db = make_labsdb_dbs_p(input_code)
        
        if db == expected_db:
            print(f"  ✓ {input_code:15} → {db:20} ({lang_name})")
            passed += 1
        else:
            print(f"  ❌ {input_code:15} → {db:20} (expected: {expected_db}) ({lang_name})")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0


def test_hyphenated_codes():
    """Test hyphenated language codes"""
    print("\n" + "=" * 70)
    print("TESTING HYPHENATED LANGUAGE CODES")
    print("=" * 70)
    
    hyphenated = [
        ("zh-min-nan", "zh_min_nanwiki_p", "Min Nan Chinese"),
        ("zh-yue", "zh_yuewiki_p", "Cantonese"),
        ("be-x-old", "be_x_oldwiki_p", "Belarusian (Taraškievica)"),
        ("be-tarask", "be_x_oldwiki_p", "Belarusian (Taraškievica)"),
        ("roa-rup", "roa_rupwiki_p", "Aromanian"),
        ("roa-tara", "roa_tarawiki_p", "Tarantino"),
        ("bat-smg", "bat_smgwiki_p", "Samogitian"),
        ("cbk-zam", "cbk_zamwiki_p", "Chavacano"),
        ("fiu-vro", "fiu_vrowiki_p", "Võro"),
        ("map-bms", "map_bmswiki_p", "Banyumasan"),
        ("nds-nl", "nds_nlwiki_p", "Low Saxon"),
    ]
    
    passed = 0
    failed = 0
    
    for input_code, expected_db, lang_name in hyphenated:
        host, db = make_labsdb_dbs_p(input_code)
        
        if db == expected_db:
            print(f"  ✓ {input_code:15} → {db:25} ({lang_name})")
            passed += 1
        else:
            print(f"  ❌ {input_code:15} → {db:25} (expected: {expected_db}) ({lang_name})")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0


def test_special_cases():
    """Test special cases"""
    print("\n" + "=" * 70)
    print("TESTING SPECIAL CASES")
    print("=" * 70)
    
    special = [
        ("wikidata", "wikidatawiki_p", "Wikidata"),
        ("commons", "commonswiki_p", "Wikimedia Commons"),
        ("species", "specieswiki_p", "Wikispecies"),
    ]
    
    passed = 0
    failed = 0
    
    for input_code, expected_db, name in special:
        host, db = make_labsdb_dbs_p(input_code)
        
        if db == expected_db:
            print(f"  ✓ {input_code:15} → {db:25} ({name})")
            passed += 1
        else:
            print(f"  ❌ {input_code:15} → {db:25} (expected: {expected_db}) ({name})")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0


def test_german_specifically():
    """Comprehensive test for German (the reported issue)"""
    print("\n" + "=" * 70)
    print("TESTING GERMAN SPECIFICALLY (REPORTED ISSUE)")
    print("=" * 70)
    
    test_cases = [
        ("de", "dewiki.analytics.db.svc.wikimedia.cloud", "dewiki_p"),
        ("dewiki", "dewiki.analytics.db.svc.wikimedia.cloud", "dewiki_p"),
    ]
    
    all_passed = True
    
    for input_code, expected_host, expected_db in test_cases:
        host, db = make_labsdb_dbs_p(input_code)
        
        host_ok = host == expected_host
        db_ok = db == expected_db
        
        if host_ok and db_ok:
            print(f"  ✓ Input: {input_code}")
            print(f"    Host: {host}")
            print(f"    DB:   {db}")
        else:
            print(f"  ❌ Input: {input_code}")
            print(f"    Host: {host} (expected: {expected_host})")
            print(f"    DB:   {db} (expected: {expected_db})")
            all_passed = False
    
    if all_passed:
        print("\n✅ German (de/dewiki) processing is CORRECT")
        print("   The issue is NOT in the database name processing logic")
    else:
        print("\n❌ German (de/dewiki) processing has ERRORS")
        print("   This could be the root cause of missing German statistics")
    
    return all_passed


def main():
    """Run all tests"""
    print("\n🧪 WIKI DATABASE NAME PROCESSING TEST SUITE")
    print("=" * 70)
    print("Testing make_labsdb_dbs_p function from src/api_sql/wiki_sql.py")
    print("=" * 70)
    
    results = []
    
    # Run all test suites
    results.append(("German (specific)", test_german_specifically()))
    results.append(("Regular languages", test_regular_languages()))
    results.append(("With 'wiki' suffix", test_with_wiki_suffix()))
    results.append(("Hyphenated codes", test_hyphenated_codes()))
    results.append(("Special cases", test_special_cases()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {status}: {test_name}")
    
    print(f"\n📊 Overall: {total_passed}/{total_tests} test suites passed")
    
    if total_passed == total_tests:
        print("\n✅ ALL TESTS PASSED")
        print("   Database name processing is working correctly for all tested languages.")
        print("   If languages are missing, the issue is likely in:")
        print("   - Wikidata sitelink retrieval")
        print("   - SQL query execution")
        print("   - Data availability")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        print("   Database name processing has errors that need to be fixed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
