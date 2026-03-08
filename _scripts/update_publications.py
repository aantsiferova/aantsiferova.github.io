#!/usr/bin/env python3
"""
Fetch publications from Google Scholar and ISTINA, merge into papers.bib.

Usage:
    python3 _scripts/update_publications.py

Requires:
    pip3 install scholarly bibtexparser requests

Features:
    - Fetches all publications from Google Scholar for a given author ID
    - Fetches publications from ISTINA (istina.msu.ru) API
    - Merges and deduplicates entries
    - Preserves manual custom fields (selected, preview, abbr, etc.)
    - Outputs to _bibliography/papers.bib
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

# Configuration
SCHOLAR_AUTHOR_ID = "lJ-GGU8AAAAJ"
ISTINA_AUTHOR_URL = "https://istina.msu.ru/workers/94119437/"  # Update with actual ISTINA ID
BIB_FILE = Path(__file__).parent.parent / "_bibliography" / "papers.bib"

# Custom fields to preserve when merging (not standard BibTeX)
PRESERVE_FIELDS = {
    "abbr", "abstract", "additional_info", "altmetric", "annotation",
    "arxiv", "award", "award_name", "bibtex_show", "blog", "code",
    "google_scholar_id", "html", "inspirehep_id", "pdf", "poster",
    "preview", "selected", "slides", "supp", "video", "website",
}


def install_dependencies():
    """Install required packages if not available."""
    required = {"scholarly": "scholarly", "bibtexparser": "bibtexparser", "requests": "requests"}
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    if missing:
        import subprocess
        print(f"Installing missing packages: {', '.join(missing)}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install"] + missing,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def load_existing_bib(bib_path):
    """Load existing .bib file and return entries as a dict keyed by entry key."""
    import bibtexparser

    entries = {}
    if not bib_path.exists():
        return entries

    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove YAML front matter if present
    content = re.sub(r"^---\s*\n---\s*\n", "", content)

    try:
        # bibtexparser v1 API
        parser = bibtexparser.bparser.BibTexParser(common_strings=True)
        library = bibtexparser.loads(content, parser=parser)
        for entry in library.entries:
            entries[entry.get("ID", "")] = entry
    except Exception as e:
        print(f"Warning: Could not parse existing bib file: {e}")

    return entries


def normalize_title(title):
    """Normalize title for comparison."""
    # Remove LaTeX commands, braces, extra spaces
    t = re.sub(r"[{}\\]", "", title)
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


def find_existing_entry(entries, title):
    """Find an existing entry by title similarity."""
    norm_title = normalize_title(title)
    for key, entry in entries.items():
        try:
            existing_title = normalize_title(entry.get("title", ""))
        except (KeyError, AttributeError):
            continue
        if norm_title == existing_title:
            return key
    return None


def make_bib_key(author_last, title, year):
    """Generate a BibTeX key from author, title, year."""
    # Take first significant word of title (skip articles)
    skip_words = {"a", "an", "the", "on", "of", "for", "and", "in", "to", "with"}
    words = re.sub(r"[^\w\s]", "", title).split()
    title_word = ""
    for w in words:
        if w.lower() not in skip_words:
            title_word = w.capitalize()
            break
    if not title_word and words:
        title_word = words[0].capitalize()

    return f"{author_last.lower()}{title_word}{year}"


def fetch_google_scholar(author_id):
    """Fetch publications from Google Scholar."""
    from scholarly import scholarly

    print(f"Fetching publications from Google Scholar (author ID: {author_id})...")

    try:
        author = scholarly.search_author_id(author_id)
        author = scholarly.fill(author, sections=["publications"])
    except Exception as e:
        print(f"Error fetching from Google Scholar: {e}")
        return []

    publications = []
    total = len(author.get("publications", []))
    print(f"Found {total} publications on Google Scholar")

    for i, pub in enumerate(author.get("publications", []), 1):
        try:
            # Fill in publication details
            pub_filled = scholarly.fill(pub)
            time.sleep(1)  # Rate limiting

            bib = pub_filled.get("bib", {})
            title = bib.get("title", "")
            year = str(bib.get("pub_year", ""))
            authors = bib.get("author", "")
            venue = bib.get("venue", bib.get("journal", bib.get("conference", "")))
            abstract = bib.get("abstract", "")
            scholar_id = pub_filled.get("author_pub_id", "").split(":")[-1] if pub_filled.get("author_pub_id") else ""
            url = pub_filled.get("pub_url", "")
            num_citations = pub_filled.get("num_citations", 0)

            # Determine entry type
            entry_type = "article"
            if any(kw in venue.lower() for kw in ["conference", "proceedings", "workshop", "symposium"]):
                entry_type = "inproceedings"
            elif "arxiv" in venue.lower() or "preprint" in venue.lower():
                entry_type = "misc"

            publications.append({
                "title": title,
                "year": year,
                "author": authors,
                "venue": venue,
                "abstract": abstract,
                "google_scholar_id": scholar_id,
                "url": url,
                "num_citations": num_citations,
                "entry_type": entry_type,
            })
            print(f"  [{i}/{total}] {title[:60]}...")
        except Exception as e:
            print(f"  [{i}/{total}] Error: {e}")
            continue

    return publications


def fetch_istina(author_url):
    """Fetch publications from ISTINA (istina.msu.ru)."""
    import requests

    print(f"Fetching publications from ISTINA ({author_url})...")

    # ISTINA provides publication data via their web interface
    # We try to access the JSON API endpoint
    try:
        # Try to extract author ID and use API
        author_id_match = re.search(r"/workers/(\d+)/", author_url)
        if not author_id_match:
            print("Could not extract ISTINA author ID from URL")
            return []

        author_id = author_id_match.group(1)
        api_url = f"https://istina.msu.ru/api/workers/{author_id}/publications/"

        response = requests.get(api_url, timeout=30, headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; academic-site-builder)"
        })

        if response.status_code == 200:
            data = response.json()
            publications = []
            for pub in data.get("results", data if isinstance(data, list) else []):
                title = pub.get("title", pub.get("name", ""))
                if title:
                    publications.append({
                        "title": title,
                        "year": str(pub.get("year", "")),
                        "author": pub.get("authors_text", ""),
                        "venue": pub.get("journal_name", pub.get("conference_name", "")),
                        "abstract": pub.get("abstract", ""),
                        "entry_type": "article",
                    })
            print(f"Found {len(publications)} publications on ISTINA")
            return publications
        else:
            print(f"ISTINA API returned status {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching from ISTINA: {e}")
        return []


def format_author_bibtex(author_str):
    """Convert 'First Last and First Last' to 'Last, First and Last, First'."""
    if not author_str:
        return ""
    # If already in "Last, First" format, return as is
    if "," in author_str.split(" and ")[0]:
        return author_str
    authors = [a.strip() for a in author_str.split(" and ")]
    formatted = []
    for a in authors:
        parts = a.strip().split()
        if len(parts) >= 2:
            formatted.append(f"{parts[-1]}, {' '.join(parts[:-1])}")
        else:
            formatted.append(a)
    return " and ".join(formatted)


def write_bib_file(entries, output_path):
    """Write entries to a .bib file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("---\n---\n\n")

        for key, entry in sorted(entries.items(), key=lambda x: x[1].get("year", "0"), reverse=True):
            entry_type = entry.get("_type", "article")
            f.write(f"@{entry_type}{{{key},\n")

            # Write fields in a consistent order
            field_order = ["title", "author", "year", "month", "booktitle", "journal",
                          "volume", "number", "pages", "publisher", "address", "doi",
                          "url", "eprint", "archiveprefix", "primaryclass",
                          "abstract", "isbn", "langid", "copyright",
                          "abbr", "selected", "preview", "bibtex_show",
                          "google_scholar_id", "html", "pdf", "code",
                          "blog", "poster", "slides", "video", "website",
                          "award", "award_name", "additional_info",
                          "altmetric", "inspirehep_id", "supp", "annotation"]

            written = set()
            for field in field_order:
                if field in entry and field != "_type" and entry[field]:
                    val = str(entry[field])
                    if field == "title":
                        f.write(f"  {field} = {{{{{val}}}}},\n")
                    elif field in ("year", "month", "selected"):
                        f.write(f"  {field} = {{{val}}},\n")
                    else:
                        f.write(f"  {field} = {{{val}}},\n")
                    written.add(field)

            # Write any remaining fields
            for field, val in entry.items():
                if field not in written and field != "_type" and val:
                    f.write(f"  {field} = {{{val}}},\n")

            f.write("}\n\n")


def merge_publications(existing_entries, new_pubs):
    """Merge new publications into existing entries, preserving custom fields."""
    merged = {}

    # First, index existing entries by normalized title
    title_index = {}
    for key, entry in existing_entries.items():
        try:
            title = entry.get("title", "")
            title_index[normalize_title(title)] = key
        except (KeyError, AttributeError):
            pass

        # Convert bibtexparser v1 entry (dict) to our internal format
        entry_dict = {"_type": entry.get("ENTRYTYPE", "article")}
        for field, value in entry.items():
            if field not in ("ID", "ENTRYTYPE"):
                entry_dict[field] = value
        merged[key] = entry_dict

    # Add new publications
    added = 0
    skipped = 0
    for pub in new_pubs:
        norm_title = normalize_title(pub["title"])

        if norm_title in title_index:
            # Update existing entry with new data, but preserve custom fields
            existing_key = title_index[norm_title]
            existing = merged[existing_key]

            # Only add fields that don't exist yet
            if pub.get("google_scholar_id") and not existing.get("google_scholar_id"):
                existing["google_scholar_id"] = pub["google_scholar_id"]
            if pub.get("abstract") and not existing.get("abstract"):
                existing["abstract"] = pub["abstract"]
            if pub.get("url") and not existing.get("url") and not existing.get("html"):
                existing["html"] = pub["url"]
            skipped += 1
        else:
            # Create new entry
            author_parts = pub["author"].split(",")[0].split()[-1] if pub["author"] else "unknown"
            bib_key = make_bib_key(author_parts, pub["title"], pub["year"])

            # Ensure unique key
            base_key = bib_key
            counter = 1
            while bib_key in merged:
                bib_key = f"{base_key}{chr(96 + counter)}"
                counter += 1

            entry_dict = {
                "_type": pub.get("entry_type", "article"),
                "title": pub["title"],
                "author": format_author_bibtex(pub["author"]),
                "year": pub["year"],
                "bibtex_show": "true",
            }
            if pub.get("venue"):
                if pub["entry_type"] == "inproceedings":
                    entry_dict["booktitle"] = pub["venue"]
                else:
                    entry_dict["journal"] = pub["venue"]
            if pub.get("abstract"):
                entry_dict["abstract"] = pub["abstract"]
            if pub.get("google_scholar_id"):
                entry_dict["google_scholar_id"] = pub["google_scholar_id"]
            if pub.get("url"):
                entry_dict["html"] = pub["url"]

            merged[bib_key] = entry_dict
            title_index[norm_title] = bib_key
            added += 1

    print(f"\nMerge results: {added} new entries added, {skipped} existing entries updated")
    return merged


def main():
    parser = argparse.ArgumentParser(description="Update publications from Google Scholar and ISTINA")
    parser.add_argument("--scholar-id", default=SCHOLAR_AUTHOR_ID, help="Google Scholar author ID")
    parser.add_argument("--istina-url", default=ISTINA_AUTHOR_URL, help="ISTINA author page URL")
    parser.add_argument("--output", default=str(BIB_FILE), help="Output .bib file path")
    parser.add_argument("--skip-scholar", action="store_true", help="Skip Google Scholar fetch")
    parser.add_argument("--skip-istina", action="store_true", help="Skip ISTINA fetch")
    parser.add_argument("--dry-run", action="store_true", help="Don't write output file")
    args = parser.parse_args()

    install_dependencies()

    output_path = Path(args.output)

    # Load existing entries
    existing = load_existing_bib(output_path)
    print(f"Loaded {len(existing)} existing entries from {output_path}")

    all_new_pubs = []

    # Fetch from Google Scholar
    if not args.skip_scholar:
        scholar_pubs = fetch_google_scholar(args.scholar_id)
        all_new_pubs.extend(scholar_pubs)

    # Fetch from ISTINA
    if not args.skip_istina:
        istina_pubs = fetch_istina(args.istina_url)
        all_new_pubs.extend(istina_pubs)

    if not all_new_pubs:
        print("No new publications fetched. Exiting.")
        return

    # Merge
    merged = merge_publications(existing, all_new_pubs)

    if args.dry_run:
        print(f"\n[DRY RUN] Would write {len(merged)} entries to {output_path}")
    else:
        write_bib_file(merged, output_path)
        print(f"\nWrote {len(merged)} entries to {output_path}")


if __name__ == "__main__":
    main()
