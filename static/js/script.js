function updateNavbarState(){
    const nav = document.getElementById('nb');
    if(!nav) return;

    const isHomePage = window.location.pathname === '/';
    const shouldUseSolidNav = window.scrollY > 10 || window.innerWidth <= 768 || !isHomePage;

    nav.classList.toggle('bg', shouldUseSolidNav);
}

window.addEventListener('scroll', updateNavbarState);
window.addEventListener('resize', updateNavbarState);
window.addEventListener('DOMContentLoaded', updateNavbarState);

window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('img').forEach(img => {
        img.decoding = 'async';
    });
});

// toggleMenu/closeMM moved inline in base.html for instant click
// Fix desktop hash links without reload
document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('a[href^="/#"],a[href^="#"]').forEach(a=>{
    a.addEventListener('click',e=>{
      const h=a.getAttribute('href');
      const id=h.substring(h.indexOf('#')+1);
      if(id && location.pathname==='/' && document.getElementById(id)){
        e.preventDefault();
        document.getElementById(id).scrollIntoView({behavior:'smooth'});
        history.pushState(null,'','#'+id);
      }
    });
  });
});
function toggleFaq(btn){
    const item = btn.parentElement;
    const open = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
    if(!open) item.classList.add('open');
}
function submitForm(){alert('Thank you! Your booking request has been received.\nOur team will call you within 30 minutes to confirm your appointment.')}

function submitToWhatsapp() {
    const name = document.getElementById('cName').value;
    const phone = document.getElementById('cPhone').value;
    const area = document.getElementById('cArea').value;
    const details = document.getElementById('cDetails').value;
    
    if(!name || !phone || !area) {
        alert('Please fill in Your Name, Phone Number, and Area.');
        return;
    }
    
    const message = `*Smart Home Booking Request*\n\n` +
                    `*Name:* ${name}\n` +
                    `*Phone:* ${phone}\n` +
                    `*Area:* ${area}\n` +
                    `*Details:* ${details || 'N/A'}\n\n` +
                    `Please confirm my booking.`;
                    
    const encoded = encodeURIComponent(message);
    const waUrl = `https://wa.me/916238054003?text=${encoded}`;
    
    window.location.href = waUrl;
}

// TESTIMONIAL SCROLL
function scrollTestimonials(dir) {
    const grid = document.getElementById('testiGrid');
    if(!grid) return;
    const cardWidth = grid.querySelector('.tc').offsetWidth + 24;
    grid.scrollBy({ left: cardWidth * dir, behavior: 'smooth' });
}

// MODAL LOGIC
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

function showModal(id) {
    const data = serviceDetails[id];
    if(!data) return;
    
    document.getElementById('modalTitle').innerText = data.title;
    document.getElementById('modalDesc').innerText = data.desc;
    
    const list = document.getElementById('modalPoints');
    list.innerHTML = '';
    data.points.forEach(pt => {
        const li = document.createElement('li');
        li.innerText = pt;
        list.appendChild(li);
    });
    
    document.getElementById('modalOverlay').classList.add('active');
}

function closeModal() {
    document.getElementById('modalOverlay').classList.remove('active');
}

const obs=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in')})},{threshold:.07,rootMargin:'0px 0px -28px 0px'});
document.querySelectorAll('.rv,.rv-l,.rv-r').forEach(el=>obs.observe(el));
document.querySelectorAll('.svc-grid,.testi-grid,.amc-grid,.proc-grid').forEach(g=>{Array.from(g.children).forEach((c,i)=>c.style.transitionDelay=(i*.1)+'s')});

// CONTACT POPUP LOGIC
setTimeout(() => {
    const isHomePage = window.location.pathname === '/';
    const hasSeenPopup = localStorage.getItem('popupShown');
    
    if (isHomePage && !hasSeenPopup) {
        const popup = document.getElementById('contactModalOverlay');
        if(popup) {
            popup.classList.add('active');
            localStorage.setItem('popupShown', 'true');
        }
    }
}, 5000);

function closeContactModal() {
    const popup = document.getElementById('contactModalOverlay');
    if(popup) {
        popup.classList.remove('active');
        localStorage.setItem('popupShown','true');
    }
}

function submitPopupToWhatsapp() {
    const name = document.getElementById('pName').value;
    const phone = document.getElementById('pPhone').value;
    const area = document.getElementById('pArea').value;
    const details = document.getElementById('pDetails').value;
    
    if(!name || !phone || !area) {
        alert('Please fill in Your Name, Phone Number, and Area.');
        return;
    }
    
    const message = `*Smart Home Booking Request*\n\n` +
                    `*Name:* ${name}\n` +
                    `*Phone:* ${phone}\n` +
                    `*Area:* ${area}\n` +
                    `*Details:* ${details || 'N/A'}\n\n` +
                    `Please confirm my booking.`;
                    
    const encoded = encodeURIComponent(message);
    const waUrl = `https://wa.me/916238054003?text=${encoded}`;
    
    window.location.href = waUrl;
}
