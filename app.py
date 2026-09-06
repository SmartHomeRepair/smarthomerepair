from flask import Flask, render_template, Response, request, send_from_directory, redirect, url_for, session, jsonify, flash
from datetime import datetime
import os
from functools import wraps

try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    supabase: Client | None = create_client(SUPABASE_URL, SUPABASE_ANON_KEY) if SUPABASE_URL and SUPABASE_ANON_KEY else None
except Exception as e:
    supabase = None
    print(f"Supabase not configured: {e}")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-in-prod")

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

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_user"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/ogugubouvouv/fuigyfcdufuhis", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not supabase:
            flash("Supabase not configured. Set SUPABASE_URL/ANON_KEY in env/GitHub Secrets.", "error")
            return render_template("admin/login.html")
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if res.user:
                session["admin_user"] = {"email": res.user.email, "id": res.user.id}
                return redirect(url_for("admin_dashboard"))
            # keep old /admin/login from being discoverable
            # no redirect to old path
            flash("Invalid credentials", "error")
        except Exception as e:
            flash(f"Login failed: {e}", "error")
    return render_template("admin/login.html")

@app.route("/ogugubouvouv/fuigyfcdufuhis/logout")
def admin_logout():
    session.pop("admin_user", None)
    # supabase sign out if needed
    try:
        if supabase:
            supabase.auth.sign_out()
    except: pass
    return redirect(url_for("admin_login"))

@app.route("/ogugubouvouv/fuigyfcdufuhis/panel")
@login_required
def admin_dashboard():
    blogs = []
    site_texts = {}
    if supabase:
        try:
            # blogs table: id, title, slug, excerpt, body, created_at
            r = supabase.table("blogs").select("*").order("created_at", desc=True).limit(20).execute()
            blogs = r.data if r.data else []
            # site_texts table: key, value
            t = supabase.table("site_texts").select("*").execute()
            site_texts = {x["key"]: x["value"] for x in (t.data or [])}
        except Exception as e:
            flash(f"Supabase fetch error: {e}", "error")
    return render_template("admin/dashboard.html", blogs=blogs, site_texts=site_texts, user=session.get("admin_user"))

@app.route("/ogugubouvouv/fuigyfcdufuhis/blogs", methods=["POST"])
@login_required
def admin_create_blog():
    if not supabase:
        return jsonify({"error": "Supabase not configured"}), 500
    data = request.get_json() or request.form
    payload = {
        "title": data.get("title"),
        "slug": data.get("slug") or data.get("title","").lower().replace(" ","-"),
        "excerpt": data.get("excerpt",""),
        "body": data.get("body",""),
    }
    try:
        supabase.table("blogs").insert(payload).execute()
        if request.is_json:
            return jsonify({"ok": True})
        return redirect(url_for("admin_dashboard"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
