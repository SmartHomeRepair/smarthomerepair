from flask import Flask, render_template, Response, request, send_from_directory
from datetime import datetime

app = Flask(__name__)

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
        {'loc': 'https://www.smarthomerepair.in/#services', 'priority': '0.6', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/#faq', 'priority': '0.5', 'changefreq': 'monthly'},
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
    elif request.path in ['/sitemap.xml','/robots.txt']:
        resp.headers['Cache-Control'] = 'public, max-age=3600'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    return resp



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
