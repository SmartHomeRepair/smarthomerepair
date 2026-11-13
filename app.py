from flask import Flask, render_template, Response, send_from_directory, request
from datetime import datetime
import os
import secrets as _secrets

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    load_dotenv()  # also try cwd
except Exception:
    pass

app = Flask(__name__)

# Security: never use a known default secret. Random fallback if SECRET_KEY is unset.
app.secret_key = os.getenv("SECRET_KEY") or _secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/ac-repair-kochi')
def ac_repair_kochi():
    return render_template('ac-repair-kochi.html')

@app.route('/fridge-repair-kochi')
def fridge_repair_kochi():
    return render_template('fridge-repair-kochi.html')

@app.route('/washing-machine-repair-kochi')
def washing_machine_repair_kochi():
    return render_template('washing-machine-repair-kochi.html')

@app.route('/ac-gas-refill-kochi')
def ac_gas_refill_kochi():
    return render_template('ac-gas-refill-kochi.html')

@app.route('/geyser-repair-kochi')
def geyser_repair_kochi():
    return render_template('geyser-repair-kochi.html')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    pages = [
        {'loc': 'https://www.smarthomerepair.in/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/about', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': 'https://www.smarthomerepair.in/services', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/contact', 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': 'https://www.smarthomerepair.in/ac-repair-kochi', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/fridge-repair-kochi', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/washing-machine-repair-kochi', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/ac-gas-refill-kochi', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/geyser-repair-kochi', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/guide', 'priority': '0.6', 'changefreq': 'monthly'},
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        xml.append(f"  <url><loc>{p['loc']}</loc><lastmod>{datetime.now().date()}</lastmod><changefreq>{p['changefreq']}</changefreq><priority>{p['priority']}</priority></url>")
    xml.append('</urlset>')
    return Response('\n'.join(xml), mimetype='application/xml')

@app.after_request
def add_headers(resp):
    if request.path.startswith('/static/'):
        resp.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    elif request.path in ['/sitemap.xml', '/robots.txt']:
        resp.headers['Cache-Control'] = 'public, max-age=3600'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = 'DENY'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
