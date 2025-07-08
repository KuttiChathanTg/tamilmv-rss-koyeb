import time, json, requests, os
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

FORUMS = [
    "https://www.1tamilblasters.com/index.php?/forums/forum/8-tamil-new-movies-tcrip-dvdscr-hdcam-predvd.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/7-tamil-new-movies-hdrips-bdrips-dvdrips-hdtv.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/9-tamil-dubbed-movies-bdrips-hdrips-dvdscr-hdcam-in-multi-audios.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/56-tamil-old-mid-movies-bdrips-hdrips-dvdrips-hdtv.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/63-tamil-new-web-series-tv-shows.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/95-tamil-movies-dvd5-dvd9-untouched-dvds.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/75-malayalam-new-movies-tcrip-dvdscr-hdcam-predvd.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/74-malayalam-new-movies-hdrips-bdrips-dvdrips-hdtv.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/76-malayalam-dubbed-movies-bdrips-hdrips-dvdscr-hdcam.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/77-malayalam-old-mid-movies-bdrips-hdrips-dvdrips.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/98-malayalam-new-web-series-tv-shows.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/79-telugu-new-movies-tcrip-dvdscr-hdcam-predvd.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/78-telugu-new-movies-hdrips-bdrips-dvdrips-hdtv.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/80-telugu-dubbed-movies-bdrips-hdrips-dvdscr-hdcam.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/81-telugu-old-mid-movies-bdrips-hdrips-dvdrips.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/96-telugu-new-web-series-tv-shows.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/100-telugu-movies-dvd5-dvd9-untouched-dvds.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/86-hindi-new-movies-hdrips-bdrips-dvdrips-hdtv.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/87-hindi-new-movies-tcrip-dvdscr-hdcam-predvd.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/88-hindi-dubbed-movies-bdrips-hdrips-dvdscr-hdcam.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/102-hindi-old-mid-movies-bdrips-hdrips-dvdrips.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/89-hindi-new-web-series-tv-shows.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/101-hindi-movies-dvd5-dvd9-untouched-dvds.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/82-kannada-new-movies-hdrips-bdrips-dvdrips-hdtv.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/84-kannada-dubbed-movies-bdrips-hdrips-dvdscr-hdcam.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/83-kannada-new-movies-tcrip-dvdscr-hdcam-predvd.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/85-kannada-old-mid-movies-bdrips-hdrips-dvdrips.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/103-kannada-new-web-series-tv-shows.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/53-english-movies-hdrips-bdrips-dvdrips.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/52-english-movies-hdcam-dvdscr-predvd.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/92-english-web-series-tv-shows.xml"
]

BASE_URL = "https://www.1tamilblasters.com"
SEEN_FILE = "seen.json"
RSS_FILE = "rss.xml"
INTERVAL = 60  # seconds

# ✅ Load previously seen torrent links
try:
    with open(SEEN_FILE) as f:
        seen = set(json.load(f))
except:
    seen = set()

def generate_rss():
    fg = FeedGenerator()
    fg.title("TamilBlasters Torrents")
    fg.link(href=BASE_URL, rel="alternate")
    fg.description("Live RSS from TamilBlasters")

    updated = False

    for forum_url in FORUMS:
        try:
            res = requests.get(forum_url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(res.text, "html.parser")

            for topic in soup.select("a[href*='index.php?/topic/']"):
                topic_url = urljoin(BASE_URL, topic["href"])

                try:
                    topic_res = requests.get(topic_url, headers={"User-Agent": "Mozilla/5.0"})
                    topic_soup = BeautifulSoup(topic_res.text, "html.parser")

                    for link in topic_soup.select("a[href*='attachment.php']"):
                        torrent_url = urljoin(BASE_URL, link["href"])
                        torrent_name = link.get_text(strip=True)

                        if torrent_url not in seen and torrent_name.endswith(".torrent"):
                            seen.add(torrent_url)
                            fe = fg.add_entry()
                            fe.title(torrent_name)
                            fe.link(href=torrent_url)
                            fe.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
                            print("🎯 Added:", torrent_name)
                            updated = True

                except Exception as err:
                    print("❌ Error in topic:", topic_url, err)

        except Exception as e:
            print("❌ Error loading forum:", forum_url, e)

    fg.rss_file(RSS_FILE)

    if updated:
        with open(SEEN_FILE, "w") as f:
            json.dump(list(seen), f)
        print("✅ RSS updated")

def scrape_loop():
    while True:
        try:
            generate_rss()
        except Exception as e:
            print("❌ Scraper crashed:", e)
        time.sleep(INTERVAL)
