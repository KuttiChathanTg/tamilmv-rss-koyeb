from flask import Flask, send_file
import threading
from scraper import scrape_loop

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ TamilMV RSS is live!"

@app.route('/tamilmv.xml')
def rss():
    return send_file('rss.xml', mimetype='application/rss+xml')

threading.Thread(target=scrape_loop, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
