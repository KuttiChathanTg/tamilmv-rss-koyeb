import time, json, requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin

# ✅ Forum pages to scrape
FORUMS = [
    "https://www.1tamilmv.onl/index.php?/forums/forum/11-web-hd-itunes-hd-bluray/",
    "https://www.1tamilmv.onl/index.php?/forums/forum/10-predvd-dvdscr-cam-tc/",
    "https://www.1tamilmv.onl/index.php?/forums/forum/12-hd-rips-dvd-rips-br-rips/"
]

BASE_URL = "https://www.1tamilmv.onl"
SEEN_FILE = "seen.json"
RSS_FILE = "rss.xml"
INTERVAL = 60  # 1 minutes

# ✅ Load seen links to avoid duplicates
try:
    with open(SEEN_FILE) as f:
        seen = set(json.load(f))
except:
    seen = set()

def generate_rss():
    fg = FeedGenerator()
    fg.title("1TamilMV Torrents")
    fg.link(href=FORUMS[0], rel="alternate")
    fg.description("Live torrent feed from TamilMV forums")

    updated = False

    for forum_url in FORUMS:
        try:
            r = requests.get(forum_url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.text, "html.parser")

            # ✅ Extract each topic link
            for a in soup.select("div.ipsDataItem_main a[href]"):
                topic_url = urljoin(BASE_URL, a["href"])
                topic_title = a.get("title", "Unknown") + ".torrent"

                # Visit topic page to find .torrent link
                try:
                    topic_r = requests.get(topic_url, headers={"User-Agent": "Mozilla/5.0"})
                    topic_soup = BeautifulSoup(topic_r.text, "html.parser")

                    for link in topic_soup.select("a[href*='attachment.php']"):
                        torrent_url = urljoin(BASE_URL, link["href"])

                        if torrent_url not in seen:
                            seen.add(torrent_url)
                            fe = fg.add_entry()
                            fe.title(topic_title)
                            fe.link(href=torrent_url)
                            fe.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
                            updated = True
                            print("🎯 Added:", topic_title)

                except Exception as err:
                    print("❌ Error in topic page:", topic_url, err)

        except Exception as e:
            print("❌ Error fetching forum:", forum_url, e)

    # ✅ Write RSS file always
    fg.rss_file(RSS_FILE)

    if updated:
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
