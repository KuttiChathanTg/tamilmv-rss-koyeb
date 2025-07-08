from flask import Flask, send_file
import threading
import os
from scraper import scrape_loop

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ TamilMV RSS is live!"

@app.route('/tamilmv.xml')
def rss():
    return send_file(os.path.abspath('rss.xml'), mimetype='application/rss+xml')

@app.route('/health')
def health():
    return "OK", 200

# ✅ STEP: Ensure rss.xml exists
if not os.path.exists("rss.xml"):
    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write("""<rss version="2.0"><channel>
<title>TamilBlasters Torrents</title>
<link>https://www.1tamilblasters.com</link>
<description>Waiting for update...</description>
</channel></rss>""")

# ✅ Start scraper in background
threading.Thread(target=scrape_loop, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
