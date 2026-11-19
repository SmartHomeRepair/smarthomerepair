from flask import Flask, render_template, Response, send_from_directory, request, redirect, url_for
from datetime import datetime
import gzip
import os
import secrets as _secrets

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    load_dotenv()  # also try cwd
except Exception:
    pass

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


def _newest_mtime(root):
    newest = 0
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            try:
                newest = max(newest, os.path.getmtime(os.path.join(dirpath, name)))
            except OSError:
                pass
    return newest


# One version token per deploy, appended to every url_for('static', ...) call.
# Lets us cache CSS/JS immutably without serving a stale file after an update.
ASSET_VERSION = str(int(_newest_mtime(STATIC_DIR)))


@app.url_defaults
def _version_static_urls(endpoint, values):
    if endpoint != 'static' or 'filename' not in values or 'v' in values:
        return
    values['v'] = ASSET_VERSION

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


# ---------------------------------------------------------------------------
# Paid-campaign landing pages
#
# These paths are used as Google Ads final URLs. They are real pages (not
# redirects) so the ad, the headline and the page all match, but they are
# noindex + canonical to the main service page: the organic ranking stays
# with /ac-repair-kochi, /washing-machine-repair-kochi and /services, and the
# site avoids five near-duplicate pages competing for the same query.
# ---------------------------------------------------------------------------

AREAS = ["Kakkanad", "Thrikkakara", "Vazhakkala", "Edappally", "Vyttila",
         "Palarivattom", "Elamakkara", "Athani", "Maradu", "Eroor South",
         "Panampilly Nagar", "Tripunithura", "Kalamassery", "Aluva", "Ernakulam"]

REVIEWS = [
    ("Excellent AC service done by Hussain Ali.", "Jose Thomas"),
    ("Nice service and good behaviour from the staff side and AC now working perfectly.", "Sharath Sadanandan"),
    ("Very good and fast service. Mr. Sehsad did his job very well.", "Sneha Mary Joseph"),
]

CAMPAIGNS = {
    'ac-repair': {
        'path': '/ac/repair',
        'title': 'AC Repair in Kochi | Same-Day Service & 90-Day Warranty',
        'desc': 'AC repair in Kochi with a 2-hour response. Gas refill, deep cleaning, PCB repair and installation. ₹399 diagnosis waived on repair. Call 6238054003.',
        'h1': 'AC Repair in Kochi, fixed the same day',
        'kicker': 'AC Repair Campaign',
        'sub': 'Certified AC technicians reach you in 2 hours across Kakkanad, Edappally, Vyttila and all of Ernakulam. Genuine parts, upfront quotes and a 90-day warranty on every repair.',
        'image': 'images/services/ac_repair.jpg',
        'image_alt': 'Technician repairing a split AC in Kochi',
        'image_w': 1400, 'image_h': 933,
        'srcset': [('images/services/ac_repair-480.jpg', '480w'),
                   ('images/services/ac_repair-900.jpg', '900w'),
                   ('images/services/ac_repair.jpg', '1400w')],
        'canonical': '/ac-repair-kochi',
        'services': [
            ('Gas refill & leak repair', 'Leak found and sealed first, then eco-friendly refrigerant refilled at the agreed price.'),
            ('Deep cleaning / jet wash', 'Coils, filters, drain pan and blower cleaned to restore cooling and cut power bills.'),
            ('PCB & sensor repair', 'Error codes, units that will not start and erratic behaviour fixed at board level.'),
            ('Installation & uninstallation', 'Split and window units fitted or shifted with correct piping, drainage and mounting.'),
            ('Cooling issue diagnosis', 'Gas, compressor, capacitor or airflow — we find the real cause and quote only that.'),
            ('Cassette & VRV servicing', 'Ceiling cassettes and centralized VRV/VRF systems for homes, offices and showrooms.'),
        ],
        'faqs': [
            ('How much does AC repair cost in Kochi?',
             'The visit and full diagnosis is ₹399, and it is waived when you go ahead with the repair. You get a complete upfront quote before any work starts, so there are no hidden charges.'),
            ('How fast can a technician reach me?',
             'Our average response is under 2 hours for most of Kochi. In peak summer it can be up to 3 hours. After booking you receive the technician name and live updates on WhatsApp.'),
            ('Do you repair both split and window ACs?',
             'Yes. We service split, window, cassette and VRV/VRF units from every major brand, including Daikin, LG, Samsung, Voltas, Blue Star, Hitachi, O General and Panasonic.'),
            ('Is there a warranty on the repair?',
             'Every repair carries a 90-day service warranty. If the same issue comes back within 90 days we fix it at no extra cost, and new spare parts carry the manufacturer warranty.'),
            ('Which areas of Kochi do you cover?',
             'Kakkanad, Thrikkakara, Vazhakkala, Edappally, Vyttila, Palarivattom, Elamakkara, Athani, Maradu, Eroor South, Panampilly Nagar, Tripunithura, Kalamassery, Aluva and Ernakulam.'),
        ],
    },
    'washing-machine': {
        'path': '/washing/machine',
        'title': 'Washing Machine Repair in Kochi | Front & Top Load, Same Day',
        'desc': 'Washing machine repair in Kochi for front-load and top-load machines. Drum, motor, PCB, drain and noise faults fixed with a 90-day warranty. Call 6238054003.',
        'h1': 'Washing machine repair in Kochi',
        'kicker': 'Washing Machine Campaign',
        'sub': 'Front-load or top-load, all major brands. A technician reaches you within 2 hours across Kochi, diagnoses the fault on the spot and quotes before starting work.',
        'image': 'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=1200&q=80&fit=crop&auto=format',
        'image_alt': 'Washing machine repair service in Kochi',
        'image_w': 1200, 'image_h': 800,
        'canonical': '/washing-machine-repair-kochi',
        'services': [
            ('Drum & bearing repair', 'Loud banging, grinding or a drum that will not spin — bearings and spider arms replaced.'),
            ('Motor & belt replacement', 'Machine fills but the drum does not turn, or turns slowly under load.'),
            ('PCB & control board', 'Error codes, dead panels and programmes that stop mid-cycle repaired at board level.'),
            ('Drain & pump faults', 'Water not draining, standing water in the drum, or an E-code on the display.'),
            ('Leak & door seal', 'Door gasket, inlet hose and internal seal leaks traced and fixed properly.'),
            ('Noise & vibration', 'Levelling, shock absorbers and balance checks so the machine stops walking across the floor.'),
        ],
        'faqs': [
            ('How much does washing machine repair cost in Kochi?',
             'Diagnosis is ₹399 and is waived when you proceed with the repair. After checking the machine the technician gives you a fixed quote for parts and labour before any work begins.'),
            ('Do you repair both front-load and top-load machines?',
             'Yes. We repair front-load, top-load and semi-automatic machines from LG, Samsung, IFB, Bosch, Whirlpool, Haier, Godrej and every other major brand.'),
            ('My machine is not draining water. Can you fix it today?',
             'In most cases yes. Blocked filters, drain pumps and hose faults are common and usually resolved in a single visit. Book before 4pm for a same-day slot.'),
            ('Do you give a warranty on washing machine repairs?',
             'Every repair is covered by a 90-day service warranty. If the same fault returns within that period we fix it free, and replacement parts carry the manufacturer warranty.'),
            ('Which areas do you cover?',
             'All of Kochi and Ernakulam, including Kakkanad, Thrikkakara, Edappally, Vyttila, Palarivattom, Elamakkara, Maradu, Kalamassery, Aluva and Tripunithura.'),
        ],
    },
    'microwave': {
        'path': '/microwave/repair',
        'title': 'Microwave Repair in Kochi | Magnetron, Door & PCB Service',
        'desc': 'Microwave repair in Kochi for solo, grill and convection ovens. Magnetron, transformer, door interlock and touchpad faults fixed with a 90-day warranty.',
        'h1': 'Microwave repair in Kochi',
        'kicker': 'Microwave Campaign',
        'sub': 'Not heating, sparking, tripping the power or a dead touchpad — we diagnose the fault, quote upfront and repair it safely. All brands, all models.',
        'image': 'images/services/microwave_repair.jpg',
        'image_alt': 'Microwave oven repair in Kochi',
        'image_w': 1200, 'image_h': 800,
        'canonical': '/services',
        'services': [
            ('Not heating', 'Magnetron, high-voltage diode and capacitor tested and replaced only when needed.'),
            ('Sparking inside', 'Burnt waveguide covers, damaged racks and dirty cavities cleaned and repaired.'),
            ('Door interlock faults', 'A microwave that runs with the door open, or will not start at all, is a safety job.'),
            ('Touchpad & control panel', 'Dead buttons, blank displays and control boards repaired or replaced.'),
            ('Turntable & motor', 'Turntable not rotating, grinding noise or a motor that has seized.'),
            ('Convection & grill faults', 'Heating elements, fans and thermostats checked for even, safe cooking.'),
        ],
        'faqs': [
            ('Is it worth repairing a microwave in Kochi?',
             'Usually yes. Magnetron, door switch and control-board repairs cost far less than a new oven, and we tell you honestly when a replacement makes more sense.'),
            ('How much is the diagnosis?',
             'The visit and diagnosis is ₹399, waived when you go ahead with the repair. The final quote is agreed before any work starts.'),
            ('Do you repair convection and grill microwaves?',
             'Yes. Solo, grill and convection models from Samsung, LG, IFB, Whirlpool, Panasonic, Bosch and other major brands.'),
            ('Is it safe to use a microwave that sparks?',
             'No. Stop using it and unplug it. Sparking can be a burnt waveguide or a failing capacitor, and both need a qualified technician.'),
            ('Which areas do you cover?',
             'Kochi and Ernakulam — Kakkanad, Thrikkakara, Edappally, Vyttila, Palarivattom, Elamakkara, Maradu, Kalamassery, Aluva, Tripunithura and nearby.'),
        ],
    },
    '24x7': {
        'path': '/24x7/repairing',
        'title': '24x7 AC & Washing Machine Repair in Kochi | Night Service',
        'desc': '24x7 AC and washing machine repair in Kochi. Night, Sunday and holiday callouts across Ernakulam with a 2-hour response. Call 6238054003.',
        'h1': '24x7 AC & washing machine repair in Kochi',
        'kicker': '24x7 Emergency Campaign',
        'sub': 'Breakdown at midnight? We answer at 2am, on Sundays and on public holidays. AC and washing machine technicians on call across Kochi, with the same upfront pricing as day service.',
        'image': 'images/ac_repair_2.jpg',
        'image_alt': 'Emergency AC repair at night in Kochi',
        'image_w': 1600, 'image_h': 1069,
        'canonical': '/services',
        'services': [
            ('Night AC repair', 'AC stopped cooling or leaking at night — a technician is dispatched, not a call-back tomorrow.'),
            ('Emergency washing machine repair', 'Flooding, a locked door or a machine that will not drain before work in the morning.'),
            ('Gas leak callouts', 'Hissing, ice on the pipes or no cooling at all — leak located and made safe.'),
            ('Electrical & PCB faults', 'Tripping breakers, burning smells and dead control boards handled safely.'),
            ('Water leakage', 'Indoor unit dripping, drain blockages and overflowing washing machines.'),
            ('Sunday & holiday service', 'The same 2-hour response and 90-day warranty, seven days a week.'),
        ],
        'faqs': [
            ('Do you really answer at night?',
             'Yes. The phone line and WhatsApp are staffed 24 hours a day, 365 days a year, including Sundays and public holidays.'),
            ('Is night service more expensive?',
             'No. The visit and diagnosis is ₹399 at any hour and is waived when you proceed with the repair. You approve the quote before work starts.'),
            ('How fast can you reach me at night?',
             'We aim for 2 hours across Kochi and Ernakulam. Late at night traffic is lighter, so response is often quicker than in the day.'),
            ('Which appliances do you repair at night?',
             'Air conditioners and washing machines are the two emergency services. Fridge, microwave and geyser calls are booked for the next available slot.'),
            ('Which areas are covered overnight?',
             'Kakkanad, Thrikkakara, Vazhakkala, Edappally, Vyttila, Palarivattom, Elamakkara, Athani, Maradu, Panampilly Nagar, Tripunithura, Kalamassery, Aluva and Ernakulam.'),
        ],
    },
}


def _render_campaign(key):
    return render_template('campaign.html', c=CAMPAIGNS[key], areas=AREAS, reviews=REVIEWS)


@app.route('/ac/repair')
def campaign_ac_repair():
    return _render_campaign('ac-repair')


@app.route('/washing/machine')
def campaign_washing_machine():
    return _render_campaign('washing-machine')


@app.route('/microwave/repair')
def campaign_microwave():
    return _render_campaign('microwave')


@app.route('/24x7/repairing')
def campaign_24x7():
    return _render_campaign('24x7')


# Variants people actually type (the multiplication sign, and the 27x7 typo)
# 301 to the one real page so no campaign URL ever 404s.
@app.route('/24×7/repairing')
@app.route('/24-7/repairing')
@app.route('/27x7/repairing')
@app.route('/27×7/repairing')
def campaign_24x7_aliases():
    return redirect(url_for('campaign_24x7'), code=301)

@app.route('/sitemap.xml')
def sitemap():
    pages = [
        {'loc': 'https://www.smarthomerepair.in/', 'template': 'index.html', 'priority': '1.0', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/about', 'template': 'about.html', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': 'https://www.smarthomerepair.in/services', 'template': 'services.html', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/contact', 'template': 'contact.html', 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': 'https://www.smarthomerepair.in/ac-repair-kochi', 'template': 'ac-repair-kochi.html', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/fridge-repair-kochi', 'template': 'fridge-repair-kochi.html', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/washing-machine-repair-kochi', 'template': 'washing-machine-repair-kochi.html', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/ac-gas-refill-kochi', 'template': 'ac-gas-refill-kochi.html', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/geyser-repair-kochi', 'template': 'geyser-repair-kochi.html', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': 'https://www.smarthomerepair.in/guide', 'template': 'guide.html', 'priority': '0.6', 'changefreq': 'monthly'},
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        try:
            stamp = datetime.fromtimestamp(os.path.getmtime(os.path.join(TEMPLATE_DIR, p['template']))).date()
        except OSError:
            stamp = datetime.now().date()
        xml.append(
            f"  <url><loc>{p['loc']}</loc><lastmod>{stamp}</lastmod>"
            f"<changefreq>{p['changefreq']}</changefreq><priority>{p['priority']}</priority></url>"
        )
    xml.append('</urlset>')
    return Response('\n'.join(xml), mimetype='application/xml')


@app.after_request
def add_headers(resp):
    path = request.path

    if path.startswith('/static/'):
        ext = os.path.splitext(path)[1].lower()
        if ext in ('.css', '.js'):
            # URLs carry ?v=<build>, so a year is safe and re-deploys bust it.
            resp.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        elif ext in ('.woff2', '.woff', '.ttf', '.otf'):
            resp.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        else:
            resp.headers['Cache-Control'] = 'public, max-age=2592000, stale-while-revalidate=86400'
    elif path in ('/sitemap.xml', '/robots.txt'):
        resp.headers['Cache-Control'] = 'public, max-age=3600'
    else:
        resp.headers['Cache-Control'] = 'no-cache'

    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = 'DENY'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    resp.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

    # Compress text responses when the client asks for it. Static files are
    # streamed straight from disk, so they are left untouched.
    accepts_gzip = 'gzip' in request.headers.get('Accept-Encoding', '').lower()
    ctype = (resp.headers.get('Content-Type') or '').lower()
    compressible = any(t in ctype for t in ('text/', 'application/json', 'application/xml',
                                            'application/javascript', 'image/svg+xml'))
    if (accepts_gzip and compressible and not path.startswith('/static/')
            and not resp.direct_passthrough
            and resp.status_code == 200 and not resp.headers.get('Content-Encoding')):
        body = resp.get_data()
        if len(body) > 600:
            resp.set_data(gzip.compress(body, 6))
            resp.headers['Content-Encoding'] = 'gzip'
            resp.headers['Vary'] = 'Accept-Encoding'
            resp.headers.pop('Content-Length', None)

    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG") == "1")

