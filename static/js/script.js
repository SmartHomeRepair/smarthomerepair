/* Smart Home Repair - front-end behaviour
   Kept dependency-free and defensive: every block checks the element exists. */

/* ---------- sticky header state ---------- */
/* Cache the viewport width: reading innerWidth inside a scroll handler forces
   a layout on every frame, which is exactly the kind of main-thread work that
   shows up as a bad INP on a low-end phone. */
let viewportWidth = window.innerWidth;
window.addEventListener('resize', () => { viewportWidth = window.innerWidth; }, {passive:true});

function updateNavbarState(){
    const nav = document.getElementById('nb');
    if(!nav) return;

    const isHomePage = window.location.pathname === '/';
    const shouldUseSolidNav = window.scrollY > 10 || viewportWidth <= 768 || !isHomePage;

    nav.classList.toggle('bg', shouldUseSolidNav);
}

let navTick = false;
function onScroll(){
    if(navTick) return;
    navTick = true;
    requestAnimationFrame(() => { updateNavbarState(); navTick = false; });
}

window.addEventListener('scroll', onScroll, {passive:true});
window.addEventListener('resize', updateNavbarState, {passive:true});
window.addEventListener('DOMContentLoaded', updateNavbarState);

/* ---------- images ---------- */
window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('img').forEach(img => { img.decoding = 'async'; });
});

/* ---------- in-page anchors ---------- */
document.addEventListener('DOMContentLoaded', () => {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.querySelectorAll('a[href^="/#"],a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const h = a.getAttribute('href');
            const id = h.substring(h.indexOf('#') + 1);
            if(id && location.pathname === '/' && document.getElementById(id)){
                e.preventDefault();
                document.getElementById(id).scrollIntoView({behavior: reduce ? 'auto' : 'smooth'});
                history.pushState(null, '', '#' + id);
                closeMM();
            }
        });
    });
});

/* ---------- mobile menu: focus management ---------- */
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('mmBtn');
    const menu = document.getElementById('mm');
    if(btn && menu){
        btn.addEventListener('click', () => {
            if(menu.classList.contains('open')){
                // let the CSS transition start before moving focus
                setTimeout(() => { const c = menu.querySelector('.mm-close'); if(c) c.focus(); }, 60);
            }
        });
        menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
            setTimeout(() => btn.focus(), 10);
        }));
    }
});

/* ---------- FAQ ---------- */
/* Now a native <details> accordion - no JS needed. */

/* ---------- booking forms -> WhatsApp ---------- */
function setFormError(form, message){
    let box = form.querySelector('.form-error');
    if(!box){
        box = document.createElement('p');
        box.className = 'form-error';
        box.setAttribute('role', 'alert');
        form.appendChild(box);
    }
    box.textContent = message;
    box.scrollIntoView({block:'center', behavior:'smooth'});
}

function clearFormError(form){
    const box = form.querySelector('.form-error');
    if(box) box.remove();
}

function sendBooking(form, ids){
    const nameEl = document.getElementById(ids.name);
    const phoneEl = document.getElementById(ids.phone);
    const areaEl = document.getElementById(ids.area);
    const detailsEl = document.getElementById(ids.details);
    if(!nameEl || !phoneEl || !areaEl) return false;

    clearFormError(form);

    const name = nameEl.value.trim();
    const phone = phoneEl.value.trim();
    const area = areaEl.value;
    const details = detailsEl ? detailsEl.value.trim() : '';
    const digits = phone.replace(/\D/g, '');

    if(!name || !area){
        setFormError(form, 'Please add your name and select your area in Kochi.');
        return false;
    }
    if(digits.length < 10 || digits.length > 13){
        setFormError(form, 'Please enter a valid phone number so we can confirm your booking.');
        phoneEl.focus();
        return false;
    }

    const message = '*Smart Home Booking Request*\n\n' +
                    '*Name:* ' + name + '\n' +
                    '*Phone:* ' + phone + '\n' +
                    '*Area:* ' + area + '\n' +
                    '*Details:* ' + (details || 'N/A') + '\n\n' +
                    'Please confirm my booking.';

    window.location.href = 'https://wa.me/916238054003?text=' + encodeURIComponent(message);
    return true;
}

function submitToWhatsapp(e){
    if(e) e.preventDefault();
    sendBooking(document.getElementById('bookingForm'),
        {name:'cName', phone:'cPhone', area:'cArea', details:'cDetails'});
}

function submitPopupToWhatsapp(e){
    if(e) e.preventDefault();
    sendBooking(document.getElementById('popupForm'),
        {name:'pName', phone:'pPhone', area:'pArea', details:'pDetails'});
}

function submitContactToWhatsapp(e){
    if(e) e.preventDefault();
    sendBooking(document.getElementById('contactForm'),
        {name:'cName', phone:'cPhone', area:'cArea', details:'cDetails'});
}

function submitCampaignToWhatsapp(e){
    if(e) e.preventDefault();
    sendBooking(document.getElementById('campaignForm'),
        {name:'qName', phone:'qPhone', area:'qArea', details:'qDetails'});
}

/* ---------- testimonials ---------- */
function scrollTestimonials(dir){
    const grid = document.getElementById('testiGrid');
    if(!grid) return;
    const card = grid.querySelector('.tc');
    if(!card) return;
    grid.scrollBy({ left: (card.offsetWidth + 24) * dir, behavior: 'smooth' });
}

/* ---------- service detail modal (reserved for future service cards) ---------- */
const serviceDetails = {
    'ac-split': {
        title: 'Split & Window Air Conditioners',
        desc: 'Comprehensive maintenance and repair services for all residential AC units. We ensure your cooling system operates at peak efficiency during the hottest months.',
        points: ['Chemical deep cleaning of filters & coils', 'Gas pressure check & top-up', 'Electrical component safety inspection', 'Detailed PCB error code diagnosis', 'Cooling & drainage optimization']
    },
    'ac-cassette': {
        title: 'Cassette Air Conditioners',
        desc: 'Expert care for ceiling-mounted cooling systems. Perfect for larger rooms and semi-commercial spaces where balanced airflow is crucial.',
        points: ['Four-way airflow balance check', 'Piping & drain line maintenance', 'Motor noise & vibration dampening', 'Panel cleaning & filter replacement', 'Mounting stability verification']
    },
    'ac-vrv': {
        title: 'VRV / VRF Commercial AC',
        desc: 'Advanced centralized cooling solutions for business environments, hotels, and large residences requiring intelligent temperature control across multiple zones.',
        points: ['Master controller logic verification', 'Multi-zone compressor load testing', 'Integrated system leak detection', 'Advanced control panel servicing', 'Annual maintenance planning']
    },
    'washing-machine': {
        title: 'Washing Machine Repair',
        desc: 'Fast and reliable repairs for both front-load and top-load machines. We handle all major brands and common mechanical or electronic issues.',
        points: ['Drum bearing & motor inspection', 'Inlet/outlet valve maintenance', 'Spin cycle noise reduction', 'PCB software & hardware repair', 'Gasket & seal leak prevention']
    },
    'refrigerator': {
        title: 'Refrigerator Repair',
        desc: 'Immediate diagnosis and fixing of cooling issues to prevent food spoilage. From thermostats to compressors, we handle it all.',
        points: ['Compressor gas level verification', 'Defrost heater & sensor testing', 'Door seal airtightness check', 'Thermostat calibration', 'Condenser coil specialized cleaning']
    },
    'microwave': {
        title: 'Microwave Repair',
        desc: 'Safe and professional repairs for microwave and convection ovens. We ensure all radiation shielding and heating components are within safety limits.',
        points: ['Magnetron & transformer testing', 'Door interlock switch safety check', 'Internal turntable motor repair', 'Heating consistency calibration', 'Control panel button response fixing']
    },
    'geyser': {
        title: 'Geyser & Water Heater',
        desc: 'Safe installation and multi-brand repair of storage and instant geysers. We prioritize electrical safety and pressure system stability.',
        points: ['Heating element scale removal', 'Pressure release valve (PRV) test', 'Thermostat auto-cut verification', 'Electrical leakage safety grounding', 'Tank corrosion inspection']
    }
};

function showModal(id){
    const data = serviceDetails[id];
    if(!data) return;
    const title = document.getElementById('modalTitle');
    const desc = document.getElementById('modalDesc');
    const list = document.getElementById('modalPoints');
    const overlay = document.getElementById('modalOverlay');
    if(!title || !desc || !list || !overlay) return;

    title.textContent = data.title;
    desc.textContent = data.desc;
    list.innerHTML = '';
    data.points.forEach(pt => {
        const li = document.createElement('li');
        li.textContent = pt;
        list.appendChild(li);
    });

    overlay.classList.add('active');
    document.body.classList.add('modal-open');
    const close = overlay.querySelector('.modal-close');
    if(close) close.focus();
}

function closeModal(){
    const overlay = document.getElementById('modalOverlay');
    if(overlay) overlay.classList.remove('active');
    document.body.classList.remove('modal-open');
}

function closeContactModal(){
    const popup = document.getElementById('contactModalOverlay');
    if(popup) popup.classList.remove('active');
    document.body.classList.remove('modal-open');
    localStorage.setItem('popupShown', 'true');
}

/* ---------- reveal on scroll ---------- */
const revealEls = document.querySelectorAll('.rv,.rv-l,.rv-r');

if('IntersectionObserver' in window){
    const obs = new IntersectionObserver(entries => {
        entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('in'); });
    }, {threshold: 0.01, rootMargin: '0px 0px -32px 0px'});

    revealEls.forEach(el => obs.observe(el));
} else {
    revealEls.forEach(el => el.classList.add('in'));
}

document.querySelectorAll('.svc-grid,.testi-grid,.amc-grid,.proc-grid').forEach(g => {
    Array.from(g.children).forEach((c, i) => { c.style.transitionDelay = (i * .1) + 's'; });
});

/* ---------- exit-style booking popup ----------
   Deliberately disabled on phones: a full-screen offer on load is the kind of
   intrusive interstitial Google demotes, and it blocks the tap-to-call path.
   Desktop visitors see it only after 15s AND 40% scroll. */
(function(){
    if(window.matchMedia('(max-width: 768px)').matches) return;
    if(localStorage.getItem('popupShown')) return;

    let waited = false;
    let scrolled = false;
    let shown = false;

    function openPopup(){
        if(shown) return;
        const popup = document.getElementById('contactModalOverlay');
        if(!popup) return;
        shown = true;
        popup.classList.add('active');
        document.body.classList.add('modal-open');
        localStorage.setItem('popupShown', 'true');
        const first = popup.querySelector('input');
        if(first) setTimeout(() => first.focus(), 120);
    }

    function maybeOpen(){ if(waited && scrolled) openPopup(); }

    setTimeout(() => { waited = true; maybeOpen(); }, 15000);

    window.addEventListener('scroll', () => {
        if(scrolled) return;
        if(window.scrollY > window.innerHeight * 0.4){
            scrolled = true;
            maybeOpen();
        }
    }, {passive:true});
})();

/* ---------- keyboard: Escape closes any overlay ---------- */
document.addEventListener('keydown', e => {
    if(e.key !== 'Escape') return;

    const popup = document.getElementById('contactModalOverlay');
    if(popup && popup.classList.contains('active')){ closeContactModal(); return; }

    const modal = document.getElementById('modalOverlay');
    if(modal && modal.classList.contains('active')){ closeModal(); return; }

    const menu = document.getElementById('mm');
    if(menu && menu.classList.contains('open')) closeMM();
});

/* ---------- backdrop click closes overlays ---------- */
[['modalOverlay', closeModal], ['contactModalOverlay', closeContactModal]].forEach(([id, close]) => {
    const overlay = document.getElementById(id);
    if(overlay){
        overlay.addEventListener('click', e => { if(e.target === overlay) close(); });
    }
});
