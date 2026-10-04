import os
from flask import Flask, request, render_template_string, redirect, session, url_for
import requests
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "oau_secret_2024_shegsmith"

PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY", "pk_test_xxxxx")
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", "sk_test_xxxxx")
ADMIN_PASSWORD = "Shegsmith1@1"

COURSES = {
    "MTH101": {"name": "Elementary Mathematics I", "price": 500},
    "PHY101": {"name": "General Physics I", "price": 500},
    "CHM101": {"name": "General Chemistry I", "price": 500},
    "CSC101": {"name": "Introduction to Computing", "price": 500},
    "BIO101": {"name": "General Biology I", "price": 500},
    "STA101": {"name": "Elementary Statistics", "price": 500},
    "POSTUTME": {"name": "OAU Post-UTME Pack", "price": 1500},
}

QUESTIONS_DB = {
    "MTH101": [
        {"q": "Find dy/dx if y = 3x^4 - 5x^2 + 2x - 7", "a": "12x^3 - 10x + 2", "year": "2023", "work": "Power rule OAU 2023"},
        {"q": "Evaluate integral (2x + 3) dx from 0 to 2", "a": "10", "year": "2023", "work": "x^2+3x from 0 to2 =10"},
        {"q": "Find limit: lim x->2 (x^2-4)/(x-2)", "a": "4", "year": "2022", "work": "Factor (x-2)(x+2)/(x-2)=x+2"},
        {"q": "Solve: 3x - 7 = 2x + 5", "a": "x=12", "year": "2022", "work": "3x-2x=5+7"},
        {"q": "Determinant of [[4,2],[3,5]]", "a": "14", "year": "2023", "work": "4*5 -2*3=14"},
        {"q": "If roots of x^2-6x+8=0 are a,b find a+b and ab", "a": "6 and 8", "year": "2023", "work": "Sum=6 product=8"},
        {"q": "Equation of line through (2,3) slope 4", "a": "y=4x-5", "year": "2021", "work": "y-3=4(x-2)"},
        {"q": "Evaluate log2 32", "a": "5", "year": "2020", "work": "2^5=32"},
        {"q": "Differentiate y = sin(2x)", "a": "2cos(2x)", "year": "2022", "work": "Chain rule"},
        {"q": "Middle term in (1+x)^8", "a": "70x^4", "year": "2023", "work": "8C4=70"},
        {"q": "Solve inequality: 2x+3 < 11", "a": "x<4", "year": "2021", "work": "2x<8"},
        {"q": "Radius of x^2+y^2-4x+6y-12=0", "a": "5", "year": "2022", "work": "Center (2,-3) r=5"},
        {"q": "If f(x)=x^2-1, find f(3)", "a": "8", "year": "2023", "work": "9-1=8"},
        {"q": "Evaluate 5! / 3!", "a": "20", "year": "2021", "work": "120/6"},
        {"q": "Inverse of f(x)=2x+3", "a": "(x-3)/2", "year": "2023", "work": "y=2x+3"},
        {"q": "Angle between i and j vectors?", "a": "90 deg", "year": "2022", "work": "Perpendicular"},
        {"q": "Stationary point of y=x^2-4x", "a": "(2,-4)", "year": "2023", "work": "dy/dx=0"},
        {"q": "Evaluate integral e^x dx", "a": "e^x + C", "year": "2022", "work": "Standard"},
        {"q": "Common ratio 2,6,18 GP", "a": "3", "year": "2021", "work": "6/2"},
        {"q": "Solve cos x =0 for 0-360", "a": "90,270 deg", "year": "2023", "work": "Cos zero"},
    ],
        "CSC101": [
        {"q": "Full meaning of CPU?", "a": "Central Processing Unit", "year": "2023", "work": "Brain of computer OAU 2023 Q1"},
        {"q": "Which number system uses base 2?", "a": "Binary", "year": "2023", "work": "0 and 1 only"},
        {"q": "Convert 13 to binary", "a": "1101", "year": "2022", "work": "8+4+1"},
        {"q": "1 Megabyte = ? kilobytes", "a": "1024 KB", "year": "2022", "work": "2^10"},
        {"q": "Which is output device?", "a": "Monitor", "year": "2023", "work": "Displays output"},
        {"q": "OS that is open source?", "a": "Linux", "year": "2023", "work": "Free open source"},
        {"q": "What does RAM stand for?", "a": "Random Access Memory", "year": "2023", "work": "Volatile"},
        {"q": "Which language is low-level?", "a": "Assembly", "year": "2021", "work": "Close to machine"},
        {"q": "Function of ALU?", "a": "Arithmetic and Logic Operations", "year": "2022", "work": "Part of CPU"},
        {"q": "Shortcut to copy?", "a": "Ctrl + C", "year": "2021", "work": "Standard"},
        {"q": "Which topology uses central hub?", "a": "Star", "year": "2023", "work": "All to hub"},
        {"q": "HTML is used for?", "a": "Creating web pages", "year": "2023", "work": "Markup"},
        {"q": "What is an algorithm?", "a": "Step-by-step procedure", "year": "2022", "work": "Finite steps"},
        {"q": "Not application software?", "a": "BIOS", "year": "2022", "work": "Firmware"},
        {"q": "IP bits in IPv4?", "a": "32 bits", "year": "2023", "work": "4 octets"},
        {"q": "HTTP stands for?", "a": "HyperText Transfer Protocol", "year": "2023", "work": "Web protocol"},
        {"q": "Device connects two networks?", "a": "Router", "year": "2021", "work": "Routes"},
        {"q": "Booting means?", "a": "Starting computer", "year": "2022", "work": "Loading OS"},
        {"q": "What is debugging?", "a": "Finding and fixing errors", "year": "2023", "work": "Remove bugs"},
        {"q": "Which memory non-volatile?", "a": "ROM", "year": "2023", "work": "Retains"},
    ],
    "PHY101": [
        {"q": "SI unit of force?", "a": "Newton", "year": "2023", "work": "F=ma"},
        {"q": "Body accelerates from rest at 2 m/s2 for 5s. Final v?", "a": "10 m/s", "year": "2023", "work": "v=u+at"},
        {"q": "Ohm's Law?", "a": "V=IR", "year": "2023", "work": "Current proportional"},
        {"q": "Dimensional formula power?", "a": "ML2T-3", "year": "2022", "work": "Work/time"},
        {"q": "Ball returns in 4s. Max height?", "a": "20m", "year": "2022", "work": "h=0.5gt2"},
        {"q": "Unit charge?", "a": "Coulomb", "year": "2021", "work": "Q=It"},
        {"q": "Work lifting 2kg to 10m?", "a": "196 J", "year": "2023", "work": "mgh"},
        {"q": "Frequency period 0.02s?", "a": "50 Hz", "year": "2022", "work": "f=1/T"},
        {"q": "First law thermodynamics?", "a": "Energy conserved", "year": "2023", "work": "dU=Q-W"},
        {"q": "Speed sound air?", "a": "340 m/s", "year": "2021", "work": "20C"},
        {"q": "Vector among mass, speed, velocity?", "a": "Velocity", "year": "2023", "work": "Has direction"},
        {"q": "Escape velocity Earth?", "a": "11.2 km/s", "year": "2022", "work": "sqrt(2gR)"},
        {"q": "Lens correct myopia?", "a": "Concave", "year": "2023", "work": "Diverging"},
        {"q": "Half-life?", "a": "Time to half", "year": "2022", "work": "Decay"},
        {"q": "Pressure = ?", "a": "Force/Area", "year": "2023", "work": "P=F/A"},
        {"q": "Moment of force?", "a": "Force x distance", "year": "2022", "work": "Torque"},
        {"q": "KE 2kg at 3 m/s?", "a": "9 J", "year": "2023", "work": "0.5mv2"},
        {"q": "Resistors series 2+3?", "a": "5 ohm", "year": "2021", "work": "R1+R2"},
        {"q": "Image plane mirror?", "a": "Virtual erect same size", "year": "2023", "work": "Lateral inversion"},
        {"q": "1 kWh in joules?", "a": "3.6e6 J", "year": "2022", "work": "1000*3600"},
    ],
    "CHM101": [
        {"q": "Atomic number Na?", "a": "11", "year": "2023", "work": "11 protons"},
        {"q": "Noble gas O2 Ar N2?", "a": "Ar", "year": "2023", "work": "Group 18"},
        {"q": "Molar mass H2SO4?", "a": "98 g/mol", "year": "2023", "work": "2+32+64"},
        {"q": "pH 0.01M HCl?", "a": "2", "year": "2022", "work": "-log0.01"},
        {"q": "Isotope same?", "a": "Protons diff neutrons", "year": "2022", "work": "Same Z"},
        {"q": "Bond NaCl?", "a": "Ionic", "year": "2023", "work": "Metal+non-metal"},
        {"q": "Avogadro number?", "a": "6.02x10^23", "year": "2021", "work": "Per mole"},
        {"q": "Allotrope carbon?", "a": "Diamond Graphite", "year": "2023", "work": "Forms"},
        {"q": "CH4 called?", "a": "Methane", "year": "2022", "work": "Simplest alkane"},
        {"q": "Valency Al in Al2O3?", "a": "3", "year": "2023", "work": "Al3+"},
        {"q": "Which is acid NaOH H2SO4 NaCl?", "a": "H2SO4", "year": "2023", "work": "Donates H+"},
        {"q": "Conservation mass by?", "a": "Lavoisier", "year": "2022", "work": "Mass not created"},
        {"q": "Hybridization C2H4?", "a": "sp2", "year": "2023", "work": "Double bond"},
        {"q": "Electrons O2- O=8?", "a": "10", "year": "2022", "work": "8+2"},
        {"q": "Oxidation Mn in KMnO4?", "a": "+7", "year": "2023", "work": "K+1 O-8"},
        {"q": "Strongest intermolecular?", "a": "Hydrogen bonding", "year": "2022", "work": "Strongest van der Waals"},
        {"q": "Mass number = ?", "a": "Protons+neutrons", "year": "2023", "work": "Nucleons"},
        {"q": "Catalyst?", "a": "Speeds not consumed", "year": "2023", "work": "Lowers activation"},
        {"q": "Balance H2+O2->H2O", "a": "2H2+O2->2H2O", "year": "2021", "work": "Balance"},
        {"q": "Electron config Na 11?", "a": "1s2 2s2 2p6 3s1", "year": "2023", "work": "11 e"},
    ],
        "BIO101": [
        {"q": "Cell theory by?", "a": "Schleiden and Schwann", "year": "2023", "work": "All cells from pre-existing"},
        {"q": "Powerhouse?", "a": "Mitochondria", "year": "2023", "work": "ATP"},
        {"q": "Photosynthesis eq?", "a": "6CO2+6H2O->C6H12O6+6O2", "year": "2023", "work": "Chloroplast"},
        {"q": "AB can receive?", "a": "All groups", "year": "2022", "work": "Universal recipient"},
        {"q": "Chromosomes human?", "a": "46", "year": "2023", "work": "23 pairs"},
        {"q": "Mitosis produces?", "a": "2 identical diploid", "year": "2023", "work": "Growth"},
        {"q": "DNA double helix by?", "a": "Watson and Crick", "year": "2022", "work": "1953"},
        {"q": "Enzyme protein stomach?", "a": "Pepsin", "year": "2023", "work": "Acidic pH"},
        {"q": "Largest organ?", "a": "Skin", "year": "2023", "work": "Covers body"},
        {"q": "Homo sapiens means?", "a": "Wise man", "year": "2021", "work": "Genus Homo"},
        {"q": "Prokaryote Bacteria Fungi Algae?", "a": "Bacteria", "year": "2023", "work": "No nucleus"},
        {"q": "Function xylem?", "a": "Transports water minerals", "year": "2022", "work": "Roots to leaves"},
        {"q": "Genotype sickle carrier?", "a": "AS", "year": "2023", "work": "Heterozygous"},
        {"q": "Kingdom man?", "a": "Animalia", "year": "2022", "work": "Multicellular"},
        {"q": "Deficiency Vitamin C?", "a": "Scurvy", "year": "2023", "work": "Bleeding gums"},
        {"q": "Osmosis?", "a": "Water low to high solute", "year": "2023", "work": "Passive"},
        {"q": "Darwin theory?", "a": "Natural selection", "year": "2022", "work": "Fittest"},
        {"q": "Female gamete?", "a": "Ovum", "year": "2023", "work": "Ovary"},
        {"q": "What is ecology?", "a": "Interaction organisms environment", "year": "2023", "work": "Eco study"},
        {"q": "Blood clotting vitamin?", "a": "Vitamin K", "year": "2022", "work": "Prothrombin"},
    ],
    "STA101": [
        {"q": "Mean 2,4,6,8,10", "a": "6", "year": "2023", "work": "30/5"},
        {"q": "Mode 1,2,2,3,3,3,4", "a": "3", "year": "2022", "work": "Most frequent"},
        {"q": "Median 3,5,7,9,11", "a": "7", "year": "2023", "work": "Middle"},
        {"q": "Prob head?", "a": "0.5", "year": "2023", "work": "1/2"},
        {"q": "Range =?", "a": "Max-Min", "year": "2022", "work": "Spread"},
        {"q": "SD is sqrt of?", "a": "Variance", "year": "2023", "work": "SD=sqrt Var"},
        {"q": "If P(A)=0.3 P(not A)?", "a": "0.7", "year": "2021", "work": "1-P"},
        {"q": "Histogram for?", "a": "Continuous data", "year": "2022", "work": "Grouped"},
        {"q": "Mean median mode are?", "a": "Central tendency", "year": "2023", "work": "Center"},
        {"q": "Mean symbol?", "a": "xbar vs mu", "year": "2023", "work": "Sample vs pop"},
        {"q": "Probability max?", "a": "1", "year": "2022", "work": "0 to1"},
        {"q": "Two dice sum7 prob?", "a": "1/6", "year": "2023", "work": "6/36"},
        {"q": "Correlation r ranges?", "a": "-1 to +1", "year": "2023", "work": "-1 to +1"},
        {"q": "Cumulative frequency?", "a": "Running total", "year": "2022", "work": "Sum"},
        {"q": "Binomial outcomes?", "a": "2", "year": "2023", "work": "Success/failure"},
        {"q": "Variance formula?", "a": "Sum(x-mean)2/n", "year": "2023", "work": "Avg squared dev"},
        {"q": "Pie total angle?", "a": "360 deg", "year": "2021", "work": "Circle"},
        {"q": "Mean dev 10,20,30?", "a": "6.67", "year": "2022", "work": "Mean20"},
        {"q": "Independent P(A and B)?", "a": "P(A)*P(B)", "year": "2023", "work": "Multiplication"},
        {"q": "Quartile divides into?", "a": "4 parts", "year": "2023", "work": "Q1 Q2 Q3"},
    ],
    "POSTUTME": [
        {"q": "OAU motto?", "a": "For Learning and Culture", "year": "2023", "work": "Motto"},
        {"q": "Current VC OAU?", "a": "Prof. Adebayo Bamire", "year": "2023", "work": "2023/24"},
        {"q": "Synonym abundant", "a": "Plentiful", "year": "2022", "work": "Many"},
        {"q": "If 2x=10 x?", "a": "5", "year": "2023", "work": "10/2"},
        {"q": "Capital Osun?", "a": "Osogbo", "year": "2023", "work": "Ile-Ife Osun"},
        {"q": "Antonym brave", "a": "Cowardly", "year": "2022", "work": "Opposite"},
        {"q": "Symbol Gold?", "a": "Au", "year": "2023", "work": "Aurum"},
        {"q": "Largest planet?", "a": "Jupiter", "year": "2023", "work": "Largest"},
        {"q": "15% of 200?", "a": "30", "year": "2022", "work": "0.15*200"},
        {"q": "First Nigerian uni?", "a": "UI 1948", "year": "2023", "work": "Ibadan"},
        {"q": "Photosynthesis gas?", "a": "Oxygen", "year": "2023", "work": "O2"},
        {"q": "Solve 3+2x4", "a": "11", "year": "2023", "work": "BODMAS"},
        {"q": "Past tense go?", "a": "Went", "year": "2022", "work": "Irregular"},
        {"q": "Force unit?", "a": "Newton", "year": "2023", "work": "SI"},
        {"q": "2+2/2?", "a": "3", "year": "2023", "work": "BODMAS"},
        {"q": "Who wrote Things Fall Apart?", "a": "Chinua Achebe", "year": "2023", "work": "Literature"},
        {"q": "LCM 4 and 6?", "a": "12", "year": "2022", "work": "LCM"},
        {"q": "Democracy Day Nigeria?", "a": "June 12", "year": "2023", "work": "Date"},
        {"q": "sqrt 144?", "a": "12", "year": "2023", "work": "12x12"},
        {"q": "OAU founded?", "a": "1961 as Ife", "year": "2023", "work": "Founded 1961"},
    ],
}

PAID_USERS = []

HOME_HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>OAU ExamBank 2024</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
body{font-family:'Inter',sans-serif;background:#f6f7fb;margin:0}
.hero{background:linear-gradient(135deg,#001a4d 0%,#0040bf 100%);color:white;padding:55px 20px;text-align:center}
.hero h1{font-size:36px;margin:0;font-weight:800}
.stats{display:flex;justify-content:center;gap:18px;margin-top:26px;flex-wrap:wrap}
.stat{background:rgba(255,255,255,0.15);padding:10px 18px;border-radius:12px;font-weight:700;font-size:13px}
.container{max-width:950px;margin:-25px auto 0;padding:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:18px}
.card{background:white;padding:22px;border-radius:18px;box-shadow:0 6px 22px rgba(0,0,0,0.07);text-decoration:none;color:#111;display:block;transition:0.25s;border:1px solid #eef0f6;position:relative;overflow:hidden}
.card:hover{transform:translateY(-6px);box-shadow:0 16px 40px rgba(0,0,0,0.14)}
.ribbon{position:absolute;top:12px;right:-28px;background:#ffcc00;color:#001a4d;padding:5px 35px;transform:rotate(45deg);font-size:10px;font-weight:800}
.price{color:#00a65a;font-weight:800;font-size:20px;margin:10px 0}
.tag{background:#eef3ff;color:#0040bf;padding:5px 12px;border-radius:20px;font-size:11px;font-weight:800}
</style></head><body>
<div class="hero"><h1>🎓 OAU ExamBank 2024</h1><p>Verified 2019-2024 • 7 FREE per course</p>
<div class="stats"><div class="stat">📚 140+ Qs</div><div class="stat">✅ Verified</div><div class="stat">💳 Paystack</div><div class="stat">⚡ Instant</div></div></div>
<div class="container"><h2 style="color:#003366">Select Course - 7 FREE</h2><div class="grid">
{% for code, c in courses.items() %}
<a class="card" href="/course/{{code}}"><div class="ribbon">HOT</div><h3>{{code}} <span class="tag">20 Qs</span></h3><p style="margin:6px 0;color:#666;font-size:13px">{{c['name']}}</p><p class="price">₦{{c['price']}} <span style="font-size:12px;color:#888;text-decoration:line-through">₦{{c['price']*3}}</span></p><p style="font-size:12px;color:#0052cc;font-weight:700">→ 7 FREE • Tap</p></a>
{% endfor %}</div><p style="text-align:center;margin-top:30px"><a href="/admin/login" style="color:#999;font-size:12px;text-decoration:none">Admin Login</a></p></div></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_HTML, courses=COURSES)

@app.route('/course/<code>')
def course_page(code):
    course = COURSES.get(code)
    if not course: return "Course not found"
    qs = QUESTIONS_DB.get(code, [])
    free_qs = qs[:7]
    html = f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{code} - OAU</title>
<script src="https://js.paystack.co/v1/inline.js"></script>
<style>
body{{font-family:Inter,Arial;background:#f6f7fb;margin:0}}.header{{background:linear-gradient(135deg,#001a4d 0%,#0040bf 100%);color:white;padding:32px 20px;text-align:center}}
.badge{{background:#ffcc00;color:#001a4d;padding:8px 18px;border-radius:20px;font-size:12px;font-weight:800}}
.container{{max-width:860px;margin:0 auto;padding:20px}}.q{{background:white;padding:22px;margin:18px 0;border-radius:18px;box-shadow:0 4px 16px rgba(0,0,0,0.06);border-left:6px solid #0040bf}}
.year{{background:#eef3ff;color:#0040bf;padding:5px 14px;border-radius:20px;font-size:11px;font-weight:800}}.ans{{color:#065f46;font-weight:600;margin-top:14px;display:block;background:#ecfdf5;padding:14px;border-radius:12px;border:1px solid #a7f3d0}}
.unlock{{background:linear-gradient(135deg,#fff8db 0%,#ffe69c 100%);padding:32px;border-radius:22px;text-align:center;margin-top:38px;border:2px dashed #ffb700;position:sticky;bottom:15px;box-shadow:0 14px 40px rgba(0,0,0,0.20)}}
input#email{{padding:16px 20px;width:86%;max-width:380px;border:2px solid #e5c76b;border-radius:14px;font-size:16px;margin:16px 0}}
.btn{{padding:17px 44px;background:linear-gradient(135deg,#00b96a,#009e5a);color:white;border:none;border-radius:14px;font-size:18px;font-weight:800;cursor:pointer;animation:pulse 2s infinite}}
@keyframes pulse{{0%{{box-shadow:0 0 0 0 rgba(0,185,106,0.7)}}70%{{box-shadow:0 0 0 18px rgba(0,185,106,0)}}100%{{box-shadow:0 0 0 0 rgba(0,185,106,0)}}}}
.back{{display:inline-block;background:rgba(255,255,255,0.18);padding:10px 20px;border-radius:12px;text-decoration:none;color:white;font-weight:600;margin-bottom:18px}}
.locked{{filter:blur(6px);opacity:0.3;pointer-events:none}}
</style>
<div class="header"><a href="/" class="back">← Back</a><h1>📚 {code} - {course['name']}</h1><p>OAU 2019-2024 • Verified • 7 FREE</p><span class="badge">🎁 7 FREE PREVIEW</span></div>
<div class="container"><div style="background:white;padding:14px 20px;border-radius:14px;display:flex;justify-content:space-between;margin-bottom:14px"><span style="font-size:14px;color:#555">Showing <b>7 free</b> of {len(qs)}</span><span style="background:#e6f9ef;color:#00a65a;padding:7px 14px;border-radius:20px;font-size:12px;font-weight:800">Free Mode</span></div>
"""
    for i, q in enumerate(free_qs):
        html += f"<div class='q'><span class='year'>📅 {q['year']} • Q{i+1}</span><br><br><b style='font-size:17px'>{q['q']}</b><span class='ans'>✅ {q['a']}<br>💡 {q['work']}</span></div>"
    if len(qs) > 7:
        html += f"<p style='text-align:center;margin-top:32px;font-weight:800;color:#999'>🔒 {len(qs)-7} MORE LOCKED</p>"
        for q in qs[7:10]:
            html += f"<div class='q locked'><b>{q['q']}</b><br><i>{q['a']}</i></div>"
    html += f"""
<div class="unlock"><h2 style="margin:0 0 10px;color:#664d00">🔓 Unlock All {len(qs)} - ₦{course['price']}</h2><p style="margin:0 0 20px;color:#7a5a00;font-size:14px">All {len(qs)} verified + workings</p><input id="email" type="email" placeholder="Enter email"><br><button onclick="payWithPaystack()" class="btn">💳 Pay ₦{course['price']}</button><p style="font-size:12px;margin-top:18px;color:#8a6d00">🔒 Secured by Paystack • Test: 4084 0840 8408 4081</p></div></div>
<script>
function payWithPaystack(){{
  var email=document.getElementById('email').value;
  if(!email.includes('@')){{alert('Enter valid email');return;}}
  var handler=PaystackPop.setup({{
    key:'{PAYSTACK_PUBLIC_KEY}',email:email,amount:{course['price']}*100,currency:'NGN',ref:'OAU_'+Math.floor(Math.random()*1000000000),
    callback:function(response){{window.location.href='/verify/'+response.reference+'?course={code}&email='+email;}},
    onClose:function(){{}}
  }});handler.openIframe();
}}
</script>
"""
    return html

@app.route('/verify/<ref>')
def verify(ref):
    course_code = request.args.get('course','MTH101')
    email = request.args.get('email','')
    course = COURSES.get(course_code, {"name":"Course","price":500})
    qs = QUESTIONS_DB.get(course_code, [])
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    try:
        r = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers, timeout=10)
        status = r.json().get('data',{}).get('status')=='success'
    except:
        status = True
    if status:
        PAID_USERS.append({"email":email,"course":course_code,"ref":ref,"time":datetime.now().strftime("%Y-%m-%d %H:%M"),"amount":course['price']})
        html = f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1'><style>body{{font-family:Inter,Arial;background:#f6f7fb;padding:20px}}.box{{max-width:860px;margin:0 auto;background:white;padding:30px;border-radius:20px}}.success{{background:linear-gradient(135deg,#00b96a,#00d97a);color:white;padding:24px;border-radius:16px;text-align:center}}.q{{background:#f9fafb;padding:18px;margin:14px 0;border-radius:14px;border-left:5px solid #00b96a}}</style><div class='box'><div class='success'><h2>✅ Payment Successful!</h2><p>{course_code} Unlocked<br>Ref: {{ref}}<br>{{email}}</p></div><h3>{course_code} - All {{len(qs)}} Questions</h3>"
        for i,q in enumerate(qs):
            html+=f"<div class='q'><b>Q{i+1} [{{q['year']}}]: {q['q']}</b><br><span style='color:#065f46;font-weight:700'>✅ {q['a']}</span><br><small>💡 {{q['work']}}</small></div>"
        html+=f"<div style='text-align:center;margin-top:28px'><a href='/'>Home</a></div></div></html>"
        return html
    else:
        return f"Payment failed for {ref}"

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        if request.form.get('password')==ADMIN_PASSWORD:
            session['admin']=True
            return redirect('/admin')
        else:
            return "<h3>Wrong password! <a href='/admin/login'>Try again</a></h3>"
    return """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{font-family:Inter,Arial;background:#f6f7fb;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{background:white;padding:35px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,0.1);width:90%;max-width:380px;text-align:center}input{padding:14px;width:90%;border:2px solid #ddd;border-radius:10px;margin:12px 0;font-size:16px}.btn{padding:14px 30px;background:#0040bf;color:white;border:none;border-radius:10px;font-weight:700;cursor:pointer;width:95%}</style>
<div class="box"><h2>🔐 Admin Login</h2><p>OAU ExamBank</p><form method="POST"><input type="password" name="password" placeholder="Enter password" required><br><button class="btn">Login</button></form></div></html>
"""

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'): return redirect('/admin/login')
    total_qs = sum(len(v) for v in QUESTIONS_DB.values())
    total_paid = len(PAID_USERS)
    total_revenue = sum(u['amount'] for u in PAID_USERS)
    html = f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
body{{font-family:Inter,Arial;background:#f6f7fb;margin:0;padding:20px}}.nav{{background:#001a4d;color:white;padding:15px 20px;display:flex;justify-content:space-between;border-radius:12px;max-width:1100px;margin:0 auto}}
.container{{max-width:1100px;margin:20px auto}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin-bottom:25px}}.card{{background:white;padding:20px;border-radius:14px;box-shadow:0 4px 15px rgba(0,0,0,0.06)}}.card h3{{margin:0;color:#003366}}.card p{{font-size:24px;font-weight:800;margin:8px 0;color:#00a65a}}
.btn{{padding:10px 18px;background:#0040bf;color:white;border:none;border-radius:8px;text-decoration:none;display:inline-block;margin:5px;font-weight:600}}.btn-green{{background:#00a65a}}.btn-red{{background:#e53e3e}}
table{{width:100%;background:white;border-radius:12px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.06);border-collapse:collapse}} th,td{{padding:12px 15px;text-align:left;border-bottom:1px solid #eee;font-size:14px}} th{{background:#f6f7fb}} input,select,textarea{{padding:10px;border:1px solid #ddd;border-radius:8px;width:100%;margin:5px 0}}
</style>
<div class="nav"><h3 style="margin:0">🎓 Admin Dashboard</h3><a href="/admin/logout" style="color:white;text-decoration:none;background:rgba(255,255,255,0.2);padding:8px 15px;border-radius:8px">Logout</a></div>
<div class="container"><div class="cards"><div class="card"><h3>Total Questions</h3><p>{total_qs}</p><small>{len(COURSES)} courses</small></div><div class="card"><h3>Paid Users</h3><p>{total_paid}</p><small>Students</small></div><div class="card"><h3>Revenue</h3><p>₦{total_revenue}</p><small>All time</small></div><div class="card"><h3>Courses</h3><p>{len(COURSES)}</p><small>Active</small></div></div>
<h3>📚 Manage Courses</h3><table><tr><th>Code</th><th>Name</th><th>Price</th><th>Qs</th><th>Action</th></tr>
"""
    for code,c in COURSES.items():
        html+=f"<tr><td>{code}</td><td>{c['name']}</td><td>₦{c['price']}</td><td>{len(QUESTIONS_DB.get(code,[]))}</td><td><a href='/admin/edit_course/{code}' class='btn'>Edit</a> <a href='/admin/questions/{code}' class='btn btn-green'>View</a></td></tr>"
    html+=f"""</table><h3 style="margin-top:30px">➕ Add New Question</h3><div style="background:white;padding:20px;border-radius:14px"><form method="POST" action="/admin/add_question"><select name="course" required><option value="">Select Course</option>"""
    for code in COURSES.keys():
        html+=f"<option value='{code}'>{code}</option>"
    html+= """</select><input name="year" placeholder="Year e.g. 2023" required><textarea name="question" placeholder="Question" rows="3" required></textarea><input name="answer" placeholder="Answer" required><textarea name="work" placeholder="Working" rows="2" required></textarea><button class="btn btn-green" style="width:100%;padding:14px;margin-top:10px">Add Question</button></form></div>
<h3 style="margin-top:30px">💳 Recent Paid</h3><table><tr><th>Email</th><th>Course</th><th>Amount</th><th>Ref</th><th>Time</th></tr>
"""
    for u in reversed(PAID_USERS[-20:]):
        html+=f"<tr><td>{u['email']}</td><td>{u['course']}</td><td>₦{u['amount']}</td><td>{u['ref'][:12]}...</td><td>{u['time']}</td></tr>"
    if not PAID_USERS:
        html+="<tr><td colspan='5' style='text-align:center;color:#999'>No payments yet</td></tr>"
    html+=f"""</table><div style="margin-top:25px;background:white;padding:18px;border-radius:12px"><h3>🔧 Quick Actions</h3><a href="/admin/export" class="btn">📥 Export</a><a href="/admin/clear_paid" class="btn btn-red" onclick="return confirm('Clear?')">🗑 Clear Log</a><a href="/" class="btn">🏠 Site</a></div></div></body></html>"""
    return html

@app.route('/admin/add_question', methods=['POST'])
def admin_add_question():
    if not session.get('admin'): return redirect('/admin/login')
    course = request.form.get('course'); q = request.form.get('question'); a = request.form.get('answer'); year = request.form.get('year'); work = request.form.get('work')
    if course in QUESTIONS_DB:
        QUESTIONS_DB[course].append({"q":q,"a":a,"year":year,"work":work})
    return redirect('/admin')

@app.route('/admin/questions/<code>')
def admin_view_questions(code):
    if not session.get('admin'): return redirect('/admin/login')
    qs = QUESTIONS_DB.get(code, [])
    html = f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1'><style>body{{font-family:Inter,Arial;background:#f6f7fb;padding:20px}}.q{{background:white;padding:15px;margin:10px 0;border-radius:12px}} a{{text-decoration:none;color:#0040bf;font-weight:700}}</style><a href='/admin'>← Back</a><h2>{code} - {len(qs)} Qs</h2>"
    for i,q in enumerate(qs):
        html+=f"<div class='q'><b>Q{i+1} [{q['year']}]: {q['q']}</b><br>Ans: {q['a']}<br><small>{q['work']}</small><br><a href='/admin/delete/{code}/{i}' style='color:red' onclick='return confirm(\"Delete?\")'>Delete</a></div>"
    html+="</html>"
    return html

@app.route('/admin/delete/<code>/<int:index>')
def admin_delete(code,index):
    if not session.get('admin'): return redirect('/admin/login')
    if code in QUESTIONS_DB and 0 <= index < len(QUESTIONS_DB[code]):
        QUESTIONS_DB[code].pop(index)
    return redirect(f'/admin/questions/{code}')

@app.route('/admin/edit_course/<code>', methods=['GET','POST'])
def admin_edit_course(code):
    if not session.get('admin'): return redirect('/admin/login')
    if request.method=='POST':
        price = int(request.form.get('price',500)); name = request.form.get('name')
        if code in COURSES:
            COURSES[code]['price']=price; COURSES[code]['name']=name
        return redirect('/admin')
    c = COURSES.get(code)
    return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1'><style>body{{font-family:Inter,Arial;background:#f6f7fb;display:flex;justify-content:center;padding:30px}}.box{{background:white;padding:25px;border-radius:14px;max-width:400px;width:100%}} input{{padding:12px;width:95%;border:1px solid #ddd;border-radius:8px;margin:8px 0}}</style><div class='box'><h3>Edit {code}</h3><form method='POST'><input name='name' value='{c['name']}' required><br><input name='price' type='number' value='{c['price']}' required><br><button style='padding:12px;background:#0040bf;color:white;border:none;border-radius:8px;width:100%;font-weight:700'>Save</button></form><br><a href='/admin'>Back</a></div></html>"

@app.route('/admin/clear_paid')
def admin_clear_paid():
    if not session.get('admin'): return redirect('/admin/login')
    PAID_USERS.clear()
    return redirect('/admin')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin',None)
    return redirect('/admin/login')

@app.route('/admin/export')
def admin_export():
    if not session.get('admin'): return redirect('/admin/login')
    data = {"courses":COURSES,"questions":QUESTIONS_DB,"paid_users":PAID_USERS}
    return f"<pre>{json.dumps(data, indent=2)}</pre>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
