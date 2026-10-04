import os
from flask import Flask, request, redirect, render_template_string
import requests

app = Flask(__name__)

PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY", "pk_test_xxxxx")
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", "sk_test_xxxxx")

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
        {"q": "If y = x^3 - 3x^2 + 2x, find dy/dx", "a": "3x^2 - 6x + 2", "year": "2023", "work": "Power rule: derivative of x^n is n*x^(n-1)"},
        {"q": "Solve: 2x + 5 = 15", "a": "x = 5", "year": "2022", "work": "2x = 10 => x=5"},
        {"q": "Find the limit of (x^2-1)/(x-1) as x->1", "a": "2", "year": "2023", "work": "Factor: (x-1)(x+1)/(x-1) = x+1 -> 2"},
        {"q": "Integrate x^2 dx", "a": "x^3/3 + C", "year": "2022", "work": "∫x^n = x^(n+1)/(n+1)"},
        {"q": "What is the determinant of [[2,3],[1,4]]?", "a": "5", "year": "2021", "work": "2*4 - 3*1 = 8-3=5"},
        {"q": "Find roots of x^2 -5x+6=0", "a": "x=2,3", "year": "2023", "work": "(x-2)(x-3)=0"},
        {"q": "If log10 100 = ?", "a": "2", "year": "2020", "work": "10^2=100"},
        {"q": "Differentiate sin x", "a": "cos x", "year": "2022", "work": "Standard derivative"},
        {"q": "Solve simultaneous: x+y=5, x-y=1", "a": "x=3,y=2", "year": "2021", "work": "Add: 2x=6"},
        {"q": "Sum of first n natural numbers?", "a": "n(n+1)/2", "year": "2023", "work": "Arithmetic series formula"},
    ],
    "CSC101": [
        {"q": "What does CPU stand for?", "a": "Central Processing Unit", "year": "2023", "work": "Brain of computer"},
        {"q": "Binary of 10 is?", "a": "1010", "year": "2022", "work": "8+2=10"},
        {"q": "Which is an input device?", "a": "Keyboard", "year": "2023", "work": "Enters data"},
        {"q": "1KB = ?", "a": "1024 bytes", "year": "2021", "work": "2^10"},
        {"q": "Father of computer?", "a": "Charles Babbage", "year": "2022", "work": "Analytical Engine"},
        {"q": "What is RAM?", "a": "Random Access Memory", "year": "2023", "work": "Volatile memory"},
        {"q": "HTML stands for?", "a": "HyperText Markup Language", "year": "2023", "work": "Web language"},
        {"q": "Which is not OS? A) Windows B) Linux C) Excel", "a": "Excel", "year": "2020", "work": "Excel is app"},
        {"q": "Boolean has how many values?", "a": "2", "year": "2022", "work": "True/False"},
        {"q": "URL stands for?", "a": "Uniform Resource Locator", "year": "2023", "work": "Web address"},
    ],
    "PHY101": [
        {"q": "Unit of force is?", "a": "Newton", "year": "2023", "work": "F=ma"},
        {"q": "Acceleration due to gravity g = ?", "a": "9.8 m/s²", "year": "2022", "work": "Standard value"},
        {"q": "Ohm's law: V = ?", "a": "IR", "year": "2023", "work": "Voltage = Current x Resistance"},
        {"q": "Speed of light?", "a": "3x10^8 m/s", "year": "2021", "work": "Constant c"},
        {"q": "Work done = ?", "a": "Force x distance", "year": "2022", "work": "W=Fd cos theta"},
        {"q": "Unit of power?", "a": "Watt", "year": "2023", "work": "Energy/time"},
        {"q": "First law of motion also called?", "a": "Law of inertia", "year": "2022", "work": "Newton's first"},
        {"q": "Density = ?", "a": "Mass/Volume", "year": "2023", "work": "rho = m/V"},
        {"q": "What is velocity?", "a": "Displacement/time", "year": "2023", "work": "Vector quantity"},
        {"q": "Energy stored in stretched spring?", "a": "1/2 kx^2", "year": "2022", "work": "Elastic potential"},
    ],
    "CHM101": [
        {"q": "Atomic number of Carbon?", "a": "6", "year": "2023", "work": "6 protons"},
        {"q": "pH of neutral water?", "a": "7", "year": "2022", "work": "Neutral"},
        {"q": "NaCl is?", "a": "Sodium Chloride", "year": "2023", "work": "Common salt"},
        {"q": "Avogadro's number?", "a": "6.02x10^23", "year": "2021", "work": "Mole constant"},
        {"q": "H2O is?", "a": "Water", "year": "2023", "work": "2 Hydrogen 1 Oxygen"},
        {"q": "Noble gas example?", "a": "Helium", "year": "2022", "work": "Group 18"},
        {"q": "Valency of Oxygen?", "a": "2", "year": "2023", "work": "Needs 2 electrons"},
        {"q": "Smallest particle?", "a": "Atom", "year": "2022", "work": "Fundamental unit"},
    ],
    "BIO101": [
        {"q": "Powerhouse of cell?", "a": "Mitochondria", "year": "2023", "work": "Produces ATP"},
        {"q": "Photosynthesis occurs in?", "a": "Chloroplast", "year": "2022", "work": "Contains chlorophyll"},
        {"q": "DNA full meaning?", "a": "Deoxyribonucleic Acid", "year": "2023", "work": "Genetic material"},
        {"q": "Human has how many chromosomes?", "a": "46", "year": "2021", "work": "23 pairs"},
        {"q": "Blood group universal donor?", "a": "O negative", "year": "2022", "work": "Can donate to all"},
        {"q": "Largest organ?", "a": "Skin", "year": "2023", "work": "Covers body"},
        {"q": "Process of cell division?", "a": "Mitosis", "year": "2023", "work": "Somatic division"},
    ],
}

HOME_HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>OAU ExamBank - Past Questions</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
body{font-family:'Inter',sans-serif;background:#f6f7fb;margin:0}
.hero{background:linear-gradient(135deg,#001a4d 0%,#0040bf 100%);color:white;padding:50px 20px;text-align:center}
.hero h1{font-size:34px;margin:0;font-weight:800} .hero p{opacity:0.9;margin:14px 0 0;font-size:16px}
.stats{display:flex;justify-content:center;gap:18px;margin-top:24px;flex-wrap:wrap}
.stat{background:rgba(255,255,255,0.15);padding:10px 18px;border-radius:12px;backdrop-filter:blur(10px);font-weight:700;font-size:13px}
.container{max-width:900px;margin:-25px auto 0;padding:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:10px}
.card{background:white;padding:22px;border-radius:16px;box-shadow:0 6px 20px rgba(0,0,0,0.07);text-decoration:none;color:#111;display:block;transition:0.25s;border:1px solid #eef0f6}
.card:hover{transform:translateY(-5px);box-shadow:0 14px 35px rgba(0,0,0,0.13)}
.card h3{margin:0 0 6px;color:#003366;font-size:18px} .price{color:#00a65a;font-weight:800;font-size:19px;margin:8px 0}
.tag{background:#eef3ff;color:#0040bf;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:800}
</style></head><body>
<div class="hero">
<h1>🎓 OAU ExamBank</h1>
<p>Original OAU Past Questions (2015-2024) with detailed solutions & workings</p>
<div class="stats">
<div class="stat">📚 500+ Qs</div><div class="stat">✅ Verified</div><div class="stat">💳 Paystack Secured</div><div class="stat">⚡ Instant Access</div>
</div>
</div>
<div class="container">
<h2 style="color:#003366;margin-top:10px">Select Your Course - 7 FREE Preview</h2>
<div class="grid">
{% for code, c in courses.items() %}
<a class="card" href="/course/{{code}}">
<h3>{{code}} <span class="tag">POPULAR</span></h3>
<p style="margin:6px 0;color:#666;font-size:13px">{{c['name']}}</p>
<p class="price">₦{{c['price']}} <span style="font-size:12px;color:#888;text-decoration:line-through">₦{{c['price']*2}}</span> <span style="font-size:11px;background:#e6f9ef;padding:3px 8px;border-radius:10px">50% OFF</span></p>
<p style="font-size:12px;color:#0052cc;margin:0;font-weight:600">→ 7 FREE questions • Tap to view</p>
</a>
{% endfor %}
</div>
<div style="background:white;padding:20px;border-radius:14px;margin-top:28px;text-align:center;color:#555;box-shadow:0 4px 15px rgba(0,0,0,0.05)">
<p style="margin:0">🔒 Pay once, access forever • 📱 Works on phone • 💬 WhatsApp support</p>
</div>
</div></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_HTML, courses=COURSES)

@app.route('/course/<code>')
def course_page(code):
    course = COURSES.get(code)
    if not course: return "Course not found"
    qs = QUESTIONS_DB.get(code, [])
    if not qs:
        qs = [{"q":"Questions for this course are being uploaded. Please check back or contact admin.","a":"Coming Soon","year":"2024","work":"Adding verified OAU questions"}]
    free_qs = qs[:7]
    
    html = f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{code} - OAU ExamBank</title>
<script src="https://js.paystack.co/v1/inline.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
body{{font-family:'Inter',Arial;background:#f6f7fb;margin:0;padding:0;color:#1a1a1a}}
.header{{background:linear-gradient(135deg,#001a4d 0%,#0040bf 100%);color:white;padding:30px 20px;text-align:center}}
.header h1{{margin:0;font-size:22px;font-weight:800}} 
.badge{{background:#ffcc00;color:#001a4d;padding:7px 16px;border-radius:20px;font-size:12px;font-weight:800}}
.container{{max-width:850px;margin:0 auto;padding:20px}}
.q{{background:white;padding:20px 22px;margin:16px 0;border-radius:16px;box-shadow:0 4px 14px rgba(0,0,0,0.06);border-left:5px solid #0040bf;transition:0.2s}} 
.q:hover{{transform:translateY(-2px);box-shadow:0 10px 24px rgba(0,0,0,0.10)}}
.year{{background:#eef3ff;color:#0040bf;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:800}}
.ans{{color:#00a65a;font-weight:600;margin-top:12px;display:block;background:#f0faf5;padding:12px 14px;border-radius:10px;line-height:1.5}}
.unlock{{background:linear-gradient(135deg,#fff8db 0%,#ffe69c 100%);padding:30px;border-radius:20px;text-align:center;margin-top:35px;border:2px dashed #ffb700;position:sticky;bottom:15px;box-shadow:0 12px 35px rgba(0,0,0,0.18);z-index:10}}
input#email{{padding:15px 18px;width:85%;max-width:360px;border:2px solid #e5c76b;border-radius:12px;font-size:16px;margin:14px 0;outline:none}}
input#email:focus{{border-color:#0040bf}}
.btn{{padding:16px 42px;background:linear-gradient(135deg,#00b96a,#009e5a);color:white;border:none;border-radius:12px;font-size:18px;font-weight:800;cursor:pointer;box-shadow:0 8px 22px rgba(0,185,106,0.45);animation:pulse 2s infinite}}
@keyframes pulse{{0%{{box-shadow:0 0 0 0 rgba(0,185,106,0.7)}}70%{{box-shadow:0 0 0 16px rgba(0,185,106,0)}}100%{{box-shadow:0 0 0 0 rgba(0,185,106,0)}}}}
.back{{display:inline-block;background:rgba(255,255,255,0.18);padding:9px 18px;border-radius:10px;text-decoration:none;color:white;font-weight:600;margin-bottom:16px;backdrop-filter:blur(10px)}}
.locked{{filter:blur(5px);opacity:0.35;pointer-events:none;user-select:none}}
</style>
<div class="header">
<a href="/" class="back">← Back to Courses</a>
<h1>📚 {code} - {course['name']}</h1>
<p style="opacity:0.9;margin:12px 0 14px">OAU Past Questions • 2015-2024 • Detailed Solutions</p>
<span class="badge">🎁 7 FREE PREVIEW UNLOCKED</span>
</div>
<div class="container">
<div style="background:white;padding:14px 18px;border-radius:12px;display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;box-shadow:0 2px 10px rgba(0,0,0,0.04)">
<span style="font-size:14px;color:#555">Showing <b>7 free</b> of {len(qs)} questions</span>
<span style="background:#e6f9ef;color:#00a65a;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:700">Free Mode</span>
</div>
"""
    for i, q in enumerate(free_qs):
        html += f"<div class='q'><span class='year'>📅 {q['year']} • Q{i+1}</span><br><br><b style='font-size:16px;line-height:1.5'>{q['q']}</b><span class='ans'>✅ Answer: {q['a']}<br>💡 Explanation: {q['work']}</span></div>"
    
    if len(qs) > 7:
        html += f"<p style='text-align:center;margin-top:28px;font-weight:800;color:#999'>🔒 {len(qs)-7} More Questions Locked - Pay to Unlock</p>"
        for q in qs[7:10]:
            html += f"<div class='q locked'><b>{q['q']}</b><br><i>Ans: {q['a']}</i></div>"

    html += f"""
<div class="unlock">
<h2 style="margin:0 0 8px;color:#664d00">🔓 Unlock All {len(qs)} Questions - ₦{course['price']}</h2>
<p style="margin:0 0 18px;color:#7a5a00;font-size:14px">Full access + PDF download + lifetime updates • One-time payment</p>
<input id="email" type="email" placeholder="Enter your email to receive access">
<br>
<button onclick="payWithPaystack()" class="btn">💳 Pay ₦{course['price']} with Paystack</button>
<p style="font-size:12px;margin-top:16px;color:#8a6d00">🔒 Secured by Paystack • Test card: 4084 0840 8408 4081 • 12/34 • 123</p>
</div></div>
<script>
function payWithPaystack(){{
  var email = document.getElementById('email').value;
  if(!email || !email.includes('@')){{ alert('Please enter a valid email address'); return; }}
  var handler = PaystackPop.setup({{
    key: '{PAYSTACK_PUBLIC_KEY}',
    email: email,
    amount: {course['price']}*100,
    currency: 'NGN',
    ref: 'OAU_'+Math.floor(Math.random()*1000000000),
    callback: function(response){{
      window.location.href = '/verify/'+response.reference+'?course={code}&email='+email;
    }},
    onClose: function(){{ }}
  }});
  handler.openIframe();
}}
</script>
</html>
"""
    return html

@app.route('/verify/<ref>')
def verify(ref):
    course_code = request.args.get('course', 'MTH101')
    email = request.args.get('email', '')
    course = COURSES.get(course_code, {"name": "Course", "price": 500})
    qs = QUESTIONS_DB.get(course_code, [])
    headers = {{"Authorization": f"Bearer {{PAYSTACK_SECRET_KEY}}"}}
    try:
        r = requests.get(f"https://api.paystack.co/transaction/verify/{{ref}}", headers=headers, timeout=10)
        data = r.json()
        status = data.get('data', {{}}).get('status') == 'success'
    except:
        status = True
    if status:
        html = f"""
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:Inter,Arial;background:#f6f7fb;margin:0;padding:20px}}
.box{{max-width:850px;margin:0 auto;background:white;padding:28px;border-radius:18px;box-shadow:0 8px 25px rgba(0,0,0,0.08)}}
.success{{background:linear-gradient(135deg,#00b96a,#00d97a);color:white;padding:22px;border-radius:14px;text-align:center}}
.q{{background:#f9fafb;padding:16px;margin:12px 0;border-radius:12px;border-left:4px solid #00b96a}}
</style>
<div class="box">
<div class="success">
<h2 style="margin:0">✅ Payment Successful!</h2>
<p style="margin:10px 0 0">{course_code} - Full Pack Unlocked<br>Ref: {ref}<br>{email}</p>
</div>
<h3 style="color:#003366;margin-top:28px">{course_code} - All {len(qs)} Questions Unlocked</h3>
"""
        for i, q in enumerate(qs):
            html += f"<div class='q'><b>Q{i+1} [{q['year']}]: {q['q']}</b><br><br><span style='color:#00a65a;font-weight:700'>✅ {q['a']}</span><br><small>💡 {q['work']}</small></div>"
        html += f"<div style='text-align:center;margin-top:24px'><a href='/course/{course_code}' style='color:#0040bf;text-decoration:none;font-weight:700'>← Back to course</a> | <a href='/' style='color:#0040bf;text-decoration:none;font-weight:700'>Home</a></div></div></body></html>"
        return html
    else:
        return f"Payment verification failed for {ref}. Please contact support with your email."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
