#!/usr/bin/env python3
"""Check RSS feed URLs for competitor blogs."""
import requests
from bs4 import BeautifulSoup
import feedparser
from urllib.parse import urljoin

competitors = {
    "Aggero": "https://aggero.io",
    "Syllaby": "https://syllaby.io",
    "Adverteyes": "https://adverteyes.ai",
    "VidMob": "https://vidmob.com"
}

# Common RSS URL patterns to try
rss_patterns = [
    "/blog/feed/",
    "/blog/rss/",
    "/blog/rss.xml",
    "/feed/",
    "/rss/",
    "/rss.xml",
    "/blog/feed",
    "/blog/rss",
    "/feed",
    "/rss",
]

def find_rss_in_html(url):
    """Look for RSS feed links in HTML."""
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for RSS links
        rss_links = []
        for link in soup.find_all('link', type=['application/rss+xml', 'application/atom+xml']):
            href = link.get('href')
            if href:
                rss_links.append(urljoin(url, href))

        # Look for <a> tags with RSS-related text
        for a in soup.find_all('a', href=True):
            if 'rss' in a.get('href', '').lower() or 'feed' in a.get('href', '').lower():
                rss_links.append(urljoin(url, a['href']))

        return rss_links
    except Exception as e:
        print(f"  ✗ Error parsing HTML: {e}")
        return []

def test_rss_url(url):
    """Test if a URL is a valid RSS feed."""
    try:
        feed = feedparser.parse(url)
        if feed.entries and len(feed.entries) > 0:
            return True, len(feed.entries)
        return False, 0
    except Exception:
        return False, 0

print("🔍 Checking RSS feeds for new competitors...\n")

results = {}

for name, base_url in competitors.items():
    print(f"📌 {name} ({base_url})")
    found_rss = None

    # Try common patterns
    print(f"  Testing common RSS patterns...")
    for pattern in rss_patterns:
        test_url = base_url + pattern
        is_valid, count = test_rss_url(test_url)
        if is_valid:
            print(f"    ✓ FOUND: {test_url} ({count} entries)")
            found_rss = test_url
            break
        else:
            print(f"    ✗ {test_url}")

    # If not found, check blog page for RSS links
    if not found_rss:
        print(f"  Checking blog page for RSS links...")
        blog_url = base_url + "/blog"
        rss_links = find_rss_in_html(blog_url)

        if rss_links:
            print(f"    Found {len(rss_links)} potential RSS links")
            for link in rss_links[:3]:  # Test first 3
                is_valid, count = test_rss_url(link)
                if is_valid:
                    print(f"    ✓ VALID: {link} ({count} entries)")
                    found_rss = link
                    break
                else:
                    print(f"    ✗ Invalid: {link}")

    # Store result
    if found_rss:
        results[name] = found_rss
        print(f"  ✅ Final: {found_rss}\n")
    else:
        results[name] = None
        print(f"  ❌ No RSS feed found\n")

print("\n" + "="*60)
print("📋 SUMMARY")
print("="*60)

for name, url in results.items():
    if url:
        print(f"✓ {name:15} {url}")
    else:
        print(f"✗ {name:15} NO RSS FEED FOUND (check manually)")

print("\n💡 If a feed wasn't found, try:")
print("   1. Visit the blog manually")
print("   2. Look for RSS icon or 'Subscribe' link")
print("   3. Check page source for <link type='application/rss+xml'>")
print("   4. Some blogs may not have RSS (use web scraping instead)")
