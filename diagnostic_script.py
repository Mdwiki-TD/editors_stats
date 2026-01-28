#!/usr/bin/env python3
"""
Diagnostic script to identify why certain languages might be missing from editor stats.

This script checks:
1. Which site JSON files exist
2. How many articles each site has
3. Which editor JSON files exist
4. How many editors each site has
5. Identifies potentially missing languages

Run this after executing the main pipeline to diagnose issues.
"""

import json
import os
from pathlib import Path

def check_site_files(sites_path):
    """Check which site sitelink files exist"""
    print("=" * 70)
    print("SITE SITELINK FILES CHECK")
    print("=" * 70)
    
    if not sites_path.exists():
        print(f"❌ Sites directory does not exist: {sites_path}")
        return {}
    
    files = list(sites_path.glob("*.json"))
    
    if not files:
        print(f"⚠️  No site files found in {sites_path}")
        return {}
    
    site_data = {}
    
    # Process ALL files into site_data for accurate major language checking
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            links = json.load(f)
        site_data[file.stem] = len(links)
    
    # Display only top 30 by size
    print(f"\nFound {len(files)} site files. Showing top 30 by article count:\n")
    
    # Common major language wikis to check
    major_wikis = {
        "dewiki": "German",
        "frwiki": "French",
        "eswiki": "Spanish",
        "itwiki": "Italian",
        "ptwiki": "Portuguese",
        "ruwiki": "Russian",
        "jawiki": "Japanese",
        "zhwiki": "Chinese",
        "arwiki": "Arabic",
        "nlwiki": "Dutch",
    }
    
    # Sort by article count and display top 30
    sorted_sites = sorted(site_data.items(), key=lambda x: x[1], reverse=True)[:30]
    for site_name, article_count in sorted_sites:
        lang_name = major_wikis.get(site_name, "")
        marker = "✓" if article_count >= 100 else "⚠️" if article_count > 0 else "❌"
        print(f"  {marker} {site_name:20} {article_count:6,} articles  {lang_name}")
    
    print(f"\n📊 Total sites with data: {len(files)}")
    
    # Check for missing major languages (uses complete site_data)
    print(f"\n🔍 Checking major languages:")
    for wiki, lang_name in major_wikis.items():
        if wiki not in site_data:
            print(f"  ❌ MISSING: {wiki:15} ({lang_name})")
        elif site_data[wiki] < 100:
            print(f"  ⚠️  LOW DATA: {wiki:15} ({lang_name}) - only {site_data[wiki]} articles")
        else:
            print(f"  ✓ OK: {wiki:15} ({lang_name}) - {site_data[wiki]:,} articles")
    
    return site_data


def check_editor_files(editors_path):
    """Check which editor files exist"""
    print("\n" + "=" * 70)
    print("EDITOR DATA FILES CHECK")
    print("=" * 70)
    
    if not editors_path.exists():
        print(f"❌ Editors directory does not exist: {editors_path}")
        return {}
    
    files = list(editors_path.glob("*.json"))
    
    if not files:
        print(f"⚠️  No editor files found in {editors_path}")
        return {}
    
    editor_data = {}
    
    # Process ALL files into editor_data for accurate major language checking
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            editors = json.load(f)
        editor_data[file.stem] = len(editors)
    
    # Display only top 30 by size
    print(f"\nFound {len(files)} editor files. Showing top 30 by editor count:\n")
    
    # Major languages to check (without "wiki" suffix as stored in editors/)
    major_langs = {
        "de": "German",
        "fr": "French",
        "es": "Spanish",
        "it": "Italian",
        "pt": "Portuguese",
        "ru": "Russian",
        "ja": "Japanese",
        "zh": "Chinese",
        "ar": "Arabic",
        "nl": "Dutch",
    }
    
    # Sort by editor count and display top 30
    sorted_editors = sorted(editor_data.items(), key=lambda x: x[1], reverse=True)[:30]
    for lang_code, editor_count in sorted_editors:
        lang_name = major_langs.get(lang_code, "")
        marker = "✓" if editor_count > 0 else "❌"
        print(f"  {marker} {lang_code:15} {editor_count:6,} editors  {lang_name}")
    
    print(f"\n📊 Total wikis with editor data: {len(files)}")
    
    # Check for missing major languages (uses complete editor_data)
    print(f"\n🔍 Checking major languages:")
    for lang, lang_name in major_langs.items():
        if lang not in editor_data:
            print(f"  ❌ MISSING: {lang:10} ({lang_name})")
        elif editor_data[lang] == 0:
            print(f"  ⚠️  NO EDITORS: {lang:10} ({lang_name})")
        else:
            print(f"  ✓ OK: {lang:10} ({lang_name}) - {editor_data[lang]:,} editors")
    
    return editor_data


def compare_site_vs_editor_data(site_data, editor_data):
    """Compare site files vs editor files to find discrepancies"""
    print("\n" + "=" * 70)
    print("DISCREPANCY ANALYSIS")
    print("=" * 70)
    
    # Convert site data (e.g., "dewiki") to match editor data (e.g., "de")
    site_codes = {name.replace("wiki", ""): count for name, count in site_data.items() if name.endswith("wiki")}
    
    # Find sites with articles but no editors
    no_editors = []
    for site, article_count in site_codes.items():
        if site not in editor_data and article_count >= 100:
            no_editors.append((site, article_count))
    
    if no_editors:
        print("\n⚠️  Sites with articles but NO editor data:")
        for site, count in sorted(no_editors, key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {site:15} {count:6,} articles → no editors")
    else:
        print("\n✓ All sites with sufficient articles have editor data")
    
    # Find sites with editors but few articles
    few_articles = []
    for editor_lang, editor_count in editor_data.items():
        if editor_lang in site_codes and site_codes[editor_lang] < 100 and editor_count > 0:
            few_articles.append((editor_lang, site_codes[editor_lang], editor_count))
    
    if few_articles:
        print("\n⚠️  Sites with editors but <100 articles:")
        for lang, articles, editors in sorted(few_articles, key=lambda x: x[2], reverse=True):
            print(f"  {lang:15} {articles:6} articles → {editors:6,} editors")


def main():
    """Main diagnostic function"""
    print("\n🔧 EDITOR STATS DIAGNOSTIC TOOL")
    print("=" * 70)
    
    # Determine paths from environment or use defaults
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # python-dotenv not installed, continue without it
        pass
    
    MAIN_PATH = os.getenv("EDITORS_STATS_PATH", "")
    main_dump_path = Path(MAIN_PATH).expanduser() if MAIN_PATH else Path("/tmp") / "editors_stats_dump"
    
    sites_path = main_dump_path / "sites"
    editors_path = main_dump_path / "editors"
    
    print(f"\nData directory: {main_dump_path}")
    print(f"Sites path: {sites_path}")
    print(f"Editors path: {editors_path}\n")
    
    # Run checks
    site_data = check_site_files(sites_path)
    editor_data = check_editor_files(editors_path)
    
    if site_data and editor_data:
        compare_site_vs_editor_data(site_data, editor_data)
    
    print("\n" + "=" * 70)
    print("✅ DIAGNOSTIC COMPLETE")
    print("=" * 70)
    
    # Provide recommendations
    print("\n📋 RECOMMENDATIONS:")
    
    if not site_data:
        print("  1. Run sitelinks.py first to generate site data")
    elif not editor_data:
        print("  1. Site data exists, but no editor data found")
        print("  2. Run by_site.py to generate editor statistics")
    else:
        print("  1. Review the discrepancies above")
        print("  2. Check logs for SQL errors or API failures")
        print("  3. Verify database connectivity for missing wikis")
        print("  4. Ensure Wikidata sitelinks are complete")


if __name__ == "__main__":
    main()
