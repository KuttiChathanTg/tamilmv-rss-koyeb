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
    # ✅ Use absolute path to avoid FileNotFoundError
    return send_file(os.path.abspath('rss.xml'), mimetype='application/rss+xml')

@app.route('/health')
def health():
    return "OK", 200

# ✅ Ensure rss.xml file exists before serving
if not os.path.exists("rss.xml"):
    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write("""<rss version="2.0"><channel>
<title>1TamilMV Torrents</title>
<link>https://www.1tamilmv.onl</link>
<description>Waiting for update...</description>
</channel></rss>""")

# Start scraping loop in background thread
threading.Thread(target=scrape_loop, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
