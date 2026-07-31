"""
News Headline Scraper

Scrapes the top headlines from Hacker News (https://news.ycombinator.com)
and saves them to a CSV file. Can run once or on a repeating schedule.

"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HN_URL = "https://news.ycombinator.com/"

# A browser-like User-Agent makes our script look like a normal visitor
# rather than a bot. Some sites block requests that don't send one.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

OUTPUT_DIR = Path("scraped_data")
OUTPUT_DIR.mkdir(exist_ok=True)


def fetch_page(url: str) -> str:
    """Download the raw HTML of a page. Raises on network/HTTP errors."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()  # raises an exception for 4xx/5xx status codes
    return response.text


def parse_headlines(html: str, limit: int = 30) -> list[dict]:
    """
    Parse Hacker News HTML and extract headline data.

    HN lays out each story as a <tr class="athing"> row containing the
    title/link, immediately followed by a second <tr> row (the "subtext")
    containing the score, author, and comment count.
    """
    soup = BeautifulSoup(html, "html.parser")
    stories = []

    story_rows = soup.select("tr.athing")[:limit]

    for row in story_rows:
        # --- Title and link ---
        title_tag = row.select_one("span.titleline a")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        link = title_tag.get("href", "")

        # --- Rank number, e.g. "1." ---
        rank_tag = row.select_one("span.rank")
        rank = rank_tag.get_text(strip=True).rstrip(".") if rank_tag else ""

        # --- The metadata row is the very next <tr> sibling ---
        subtext_row = row.find_next_sibling("tr")
        points, author, comments = "0", "unknown", "0"

        if subtext_row:
            score_tag = subtext_row.select_one("span.score")
            if score_tag:
                points = score_tag.get_text(strip=True).split()[0]

            author_tag = subtext_row.select_one("a.hnuser")
            if author_tag:
                author = author_tag.get_text(strip=True)

            # The comments link is usually the last <a> in the subtext row
            links = subtext_row.select("a")
            if links:
                comment_text = links[-1].get_text(strip=True)
                if comment_text and comment_text[0].isdigit():
                    comments = comment_text.split()[0]

        stories.append({
            "rank": rank,
            "title": title,
            "url": link,
            "points": points,
            "author": author,
            "comments": comments,
        })

    return stories


def save_to_csv(stories: list[dict], filename: str | None = None) -> Path:
    """Save scraped stories to a timestamped CSV file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hn_headlines_{timestamp}.csv"

    filepath = OUTPUT_DIR / filename
    fieldnames = ["rank", "title", "url", "points", "author", "comments"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stories)

    return filepath


def scrape_once(limit: int = 30) -> None:
    """Run a single scrape: fetch, parse, print, and save."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching Hacker News...")

    try:
        html = fetch_page(HN_URL)
    except requests.RequestException as e:
        print(f"  ERROR: Could not reach Hacker News ({e})")
        return

    stories = parse_headlines(html, limit=limit)

    if not stories:
        print("  No stories found — the site's HTML structure may have changed.")
        return

    print(f"  Found {len(stories)} stories:\n")
    for s in stories:
        print(f"  {s['rank']:>3}. {s['title']}  ({s['points']} pts, {s['comments']} comments)")

    filepath = save_to_csv(stories)
    print(f"\n  Saved to {filepath}\n")


def run_scheduled(interval_minutes: int, limit: int = 30) -> None:
    """Run the scraper on a repeating schedule until interrupted (Ctrl+C)."""
    import schedule  # imported here so `--schedule` is the only path that needs it

    schedule.every(interval_minutes).minutes.do(scrape_once, limit=limit)

    print(f"Scheduler started: scraping every {interval_minutes} minute(s).")
    print("Press Ctrl+C to stop.\n")

    scrape_once(limit=limit)  # run once immediately, then wait for the schedule
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Scrape Hacker News headlines.")
    parser.add_argument("--limit", type=int, default=30,
                         help="Number of stories to scrape (default: 30)")
    parser.add_argument("--schedule", type=int, metavar="MINUTES",
                         help="Run repeatedly every N minutes instead of once")
    args = parser.parse_args()

    if args.schedule:
        run_scheduled(args.schedule, limit=args.limit)
    else:
        scrape_once(limit=args.limit)


if __name__ == "__main__":
    main()