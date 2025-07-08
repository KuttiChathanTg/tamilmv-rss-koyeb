import time, json, requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin

TARGET_URL = "https://www.1tamilmv.onl/latest-movies/"
BASE_URL = "https://www.1tamilmv.onl"
SEEN_FILE = "seen.json"
RSS_FILE = "rss.xml"
INTERVAL = 300  # seconds

try:
    with open(SEEN_FILE) as f:
        seen = set(json.load(f))
except:
    seen = set()

def generate_rss():
    r = requests.get(TARGET_URL, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    fg = FeedGenerator()
    fg.title("1TamilMV Torrents")
    fg.link(href=TARGET_URL, rel="alternate")
    fg.description("Live torrent feed from 1TamilMV")

    updated = False
    for block in soup.select("div.movie-item"):
        title = block.find("h3").get_text(strip=True) + ".torrent"
        href = block.find("a", href=True)["href"]
        full = urljoin(BASE_URL, href)
        if "attachment.php" in full and full not in seen:
            seen.add(full)
            fe = fg.add_entry()
            fe.title(title)
            fe.link(href=full)
            fe.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
            updated = True

    if updated:
        fg.rss_file(RSS_FILE)
        with open(SEEN_FILE, "w") as f:
            json.dump(list(seen), f)

def scrape_loop():
    while True:
        try:
            generate_rss()
            print("✅ RSS updated")
        except Exception as e:
            print("❌ Error:", e)
        time.sleep(INTERVAL)
