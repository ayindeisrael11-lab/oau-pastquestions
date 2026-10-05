from flask import Flask, render_template_string, request, redirect
import os

app = Flask(__name__)

PAYSTACK_PUBLIC_KEY = os.environ.get("PAYSTACK_PUBLIC_KEY", "pk_test_YOUR_KEY_HERE")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Shegsmith1@1")

# ========= YOUR ORIGINAL 100-LEVEL COURSES FROM YOUR NOTE =========
COURSES_INFO = {
    "MTH101/102": {"name": "Elementary Mathematics", "level": "100L", "faculty": "Science"},
    "PHY101/102": {"name": "General Physics", "level": "100L", "faculty": "Science"},
    "CHM101/102": {"name": "Introduction to Chemistry", "level": "100L", "faculty": "Science"},
    "CSC101": {"name": "Introduction to Computer Science", "level": "100L", "faculty": "Technology"},
    "BOT101/102": {"name": "Introductory Botany", "level": "100L", "faculty": "Science"},
    "ZOO101/102": {"name": "Introductory Zoology", "level": "100L", "faculty": "Science"},
    "PHY105/106": {"name": "Physics for Biological Science", "level": "100L", "faculty": "Science"},
    "PHL101": {"name": "Introduction to Philosophy", "level": "100L", "faculty": "Arts"},
    "HIS109": {"name": "Introduction to Nigerian History", "level": "100L", "faculty": "Arts"},
    "PUL101": {"name": "Legal Method", "level": "100L", "faculty": "Law"},
    "MTH105/106": {"name": "Mathematics for Social Science", "level": "100L", "faculty": "Social Science"},
    "ECN101/102": {"name": "Principles of Economics", "level": "100L", "faculty": "Social Science"},
    "SOC101/102": {"name": "Introduction to Sociology", "level": "100L", "faculty": "Social Science"},
    "BUS101/102": {"name": "Introduction to Business Admin", "level": "100L", "faculty": "Admin"},
    "ACC101/102": {"name": "Principles of Accounting", "level": "100L", "faculty": "Admin"},
    "GST111": {"name": "Communication in English", "level": "100L", "faculty": "All"},
    "AMS101": {"name": "Principles of Management", "level": "100L", "faculty": "Admin"},
    "AMS103": {"name": "Introduction to Computer", "level": "100L", "faculty": "Admin"},
    "PAD101/102": {"name": "Element of Public Administration", "level": "100L", "faculty": "Admin"},
    "PAD103/104": {"name": "Mathematical Functions For Public Admin", "level": "100L", "faculty": "Admin"},
    "PAD105": {"name": "Introduction to Philosophy of Public Admin", "level": "100L", "faculty": "Admin"},
    "PAD107/108": {"name": "Introduction to Administration", "level": "100L", "faculty": "Admin"},
    "PAD111": {"name": "Element of Governance", "level": "100L", "faculty": "Admin"},
    "PAD106": {"name": "Introduction to Politics and Administration", "level": "100L", "faculty": "Admin"},
    "GST112": {"name": "Nigerian Peoples and Culture", "level": "100L", "faculty": "All"},
    "AMS102": {"name": "Basic Mathematics", "level": "100L", "faculty": "Admin"},
    "AMS104": {"name": "Principles of Project Management", "level": "100L", "faculty": "Admin"},
    "POSTUTME": {"name": "OAU Post-UTME Screening", "level": "POSTUTME", "faculty": "Aspirants"},
}

# Keep your old questions - move STA101 to MTH101/102 if needed
QUESTIONS_DB = {
    "MTH101/102": [
        {"q": "What is mean symbol for sample vs population?", "a": "x-bar for sample, μ for population", "year": "2023", "work": "Sample mean = x̄, Population = μ - You go see am for MTH101/102 exam"},
    ],
    "POSTUTME": [
        {"q": "What is OAU motto?", "a": "For Learning and Culture", "year": "2023", "work": "Official motto"},
        {"q": "Who is current VC of OAU?", "a": "Prof. Adebayo Bamire", "year": "2023", "work": "VC 2023/2024"},
        {"q": "Synonym of abundant?", "a": "Plentiful", "year": "2022", "work": "More than enough"},
        {"q": "If 2x = 10, find x", "a": "5", "year": "2023", "work": "x=10/2=5"},
        {"q": "Capital of Osun State?", "a": "Osogbo", "year": "2023", "work": "OAU dey Ife, Osun"},
    ],
}

LEVELS = {
    "100L": {"title": "100 Level", "full": "100 Level - All Departments", "desc": "MTH101/102, PHY101/102, PAD, GST, ECN etc - 27 Courses", "color": "#0B1D51", "count": 27},
    "POSTUTME": {"title": "Post-UTME", "full": "OAU Post-UTME Screening", "desc": "2015-2024 original screening questions", "color": "#8B0000", "count": 1},
}

BASE = """
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:#F8FAFC}
.container{max-width:1100px;margin:auto;padding:20px}
.header{background:linear-gradient(135deg,#0B1D51,#1e3a8a);color:white;padding:30px;border-radius:16px;text-align:center}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px;margin-top:20px}
.card{background:white;border-radius:14px;padding:22px;box-shadow:0 4px 15px rgba(0,0,0,0.06)}
.btn{display:inline-block;padding:11px 20px;background:var(--c);color:white;border-radius:9px;text-decoration:none;font-weight:700}
.q{background:white;padding:16px;margin:12px 0;border-radius:10px;border-left:4px solid #0B1D51}
.badge{background:#EEF2FF;color:#0B1D51;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:700}
</style>
<script src="https://js.paystack.co/v1/inline.js"></script>
"""

@app.route('/')
def home():
    h = f"{BASE}<div class='container'><div class='header'><h1>OAU PAST QUESTIONS HUB</h1><p>Original • With Workings • As Written: MTH101/102 Format</p><br><a href='/admin' style='background:rgba(255,255,255,0.2);padding:6px 12px;border-radius:20px;color:white;text-decoration:none;font-size:12px'>🔒 Admin Login</a></div><div class='grid'>"
    for code, lvl in LEVELS.items():
        h += f"<a href='/level/{code}' class='card' style='--c:{lvl['color']};text-decoration:none;color:black;border-top:5px solid {lvl['color']}'><div class='badge'>{lvl['count']} COURSES</div><h2 style='margin:10px 0'>{lvl['title']}</h2><p style='color:#64748B;font-size:14px'>{lvl['desc']}</p><span class='btn' style='--c:{lvl['color']}'>Browse {lvl['title']} →</span></a>"
    h += "</div></div>"
    return h

@app.route('/level/<lvl>')
def level_page(lvl):
    info = LEVELS.get(lvl)
    if not info: return "<a href='/'>Not found</a>"
    courses = {k:v for k,v in COURSES_INFO.items() if v['level']==lvl}
    h = f"{BASE}<div class='container'><div class='header' style='background:{info['color']}'><a href='/' style='color:white'>← Home</a><h1 style='margin-top:10px'>{info['full']}</h1><p>{info['desc']}</p></div><div class='grid' style='margin-top:20px'>"
    for code, c in courses.items():
        cnt = len(QUESTIONS_DB.get(code, []))
        h += f"<div class='card' style='--c:{info['color']};border-left:4px solid {info['color']}'><div class='badge'>{c['faculty']}</div><h3>{code}</h3><p style='font-size:14px'>{c['name']}</p><p style='font-size:13px;margin:8px 0;color:{'green' if cnt>0 else '#B45309'}'>● {cnt if cnt>0 else '0'} Questions</p><a href='/course/{code}' class='btn' style='--c:{info['color']}'>Open →</a></div>"
    h += "</div></div>"
    return h

@app.route('/course/<path:code>')
def course_page(code):
    qs = QUESTIONS_DB.get(code, [])
    info = COURSES_INFO.get(code)
    if not info: return f"Course {code} not found <a href='/'>Go Home</a>"
    lvl = LEVELS.get(info['level'])
    h = f"{BASE}<div class='container'><div class='header' style='background:{lvl['color']}'><a href='/level/{info['level']}' style='color:white'>← {info['level']}</a> | <a href='/' style='color:white'>Home</a><h2 style='margin-top:10px'>{code} - {info['name']}</h2><p>{len(qs)} Past Questions Available</p></div>"
    for i, q in enumerate(qs, 1):
        h += f"<div class='q'><span class='badge'>{q['year']}</span> Q{i}<p style='margin:10px 0;font-weight:600'>{q['q']}</p><details><summary style='cursor:pointer;color:#0B1D51;font-weight:700'>Show Answer & Working</summary><div style='background:#F0FDF4;padding:12px;border-radius:8px;margin-top:8px'><b>Ans: {q['a']}</b><br><br>{q['work']}</div></details></div>"
    if qs:
        h += f"<div style='background:white;padding:24px;border-radius:14px;text-align:center;margin-top:20px'><h3>Download Full {code} PDF (100+ Qs)</h3><button onclick=\"payWithPaystack()\" style='padding:14px 28px;background:#22C55E;color:white;border:none;border-radius:10px;font-weight:700;margin-top:10px;cursor:pointer'>Pay ₦500 with Paystack</button><script>function payWithPaystack(){{var handler=PaystackPop.setup({{key:'{PAYSTACK_PUBLIC_KEY}',email:'student@oau.com',amount:50000,currency:'NGN',ref:'OAU_'+Math.floor(Math.random()*1000000000),callback:function(r){{alert('Payment successful! Ref: '+r.reference)}},onClose:function(){{alert('Closed')}}}});handler.openIframe();}}</script></div>"
    else:
        h += f"<div style='background:white;padding:30px;text-align:center;border-radius:14px;margin-top:20px'><h3>📚 {code} Questions Loading</h3><p style='color:#64748B'>We are uploading original questions for {code}. Check back or contact admin.</p></div>"
    h += "</div>"
    return h

@app.route('/admin', methods=['GET','POST'])
def admin():
    is_logged = request.args.get('logged') == '1'
    if request.method == 'POST':
        pwd = request.form.get('password')
        is_add = request.form.get('course_code') is not None
        if not is_add:
            if pwd != ADMIN_PASSWORD:
                return f"{BASE}<div class='container'><div class='card' style='max-width:400px;margin:50px auto;text-align:center'><h3>❌ Wrong Password</h3><a href='/admin' class='btn' style='--c:#0B1D51'>Try again</a></div></div>"
            return redirect('/admin?logged=1')
        else:
            if pwd != ADMIN_PASSWORD:
                return f"{BASE}<div class='container'><div class='card'><h3>❌ Access denied</h3><a href='/admin'>Login again</a></div></div>"
            course_code = request.form.get('course_code')
            q = request.form.get('q'); a = request.form.get('a'); year = request.form.get('year','2023'); work = request.form.get('work','')
            if course_code and q:
                if course_code not in QUESTIONS_DB: QUESTIONS_DB[course_code]=[]
                QUESTIONS_DB[course_code].append({"q":q,"a":a,"year":year,"work":work})
                return f"{BASE}<div class='container'><div class='card'><h3>✅ Added to {course_code}!</h3><p>{q}</p><a href='/admin?logged=1' class='btn' style='--c:#0B1D51'>Add More</a> <a href='/course/{course_code}' class='btn' style='--c:green'>View</a></div></div>"
    if not is_logged:
        return f"""{BASE}<div class='container'><div class='card' style='max-width:400px;margin:60px auto;text-align:center'>
        <h2>🔒 Admin Login</h2><p style='color:#64748B;margin:10px 0'>Enter password to continue</p>
        <form method='POST'><input name='password' type='password' placeholder='Enter admin password' required style='width:100%;padding:12px;border-radius:8px;border:1px solid #ccc'><br><br>
        <button type='submit' style='width:100%;padding:12px;background:#0B1D51;color:white;border:none;border-radius:8px;font-weight:700'>Login</button></form>
        <a href='/' style='display:inline-block;margin-top:15px'>← Home</a></div></div>"""
    opts = "".join([f"<option>{c}</option>" for c in COURSES_INFO.keys()])
    return f"""{BASE}<div class='container'><div class='header'><h2>✅ Admin Panel - Add Questions</h2><p>Welcome Admin!</p></div>
    <div class='card' style='margin-top:20px;max-width:600px'>
    <form method='POST'><input name='password' type='hidden' value='{ADMIN_PASSWORD}'>
    <label>Course Code</label><br><select name='course_code' style='width:100%;padding:10px;margin:6px 0 14px 0;border-radius:8px;border:1px solid #ccc'>{opts}</select><br>
    <label>Year</label><br><input name='year' value='2023' style='width:100%;padding:10px;margin:6px 0 14px 0;border-radius:8px;border:1px solid #ccc'><br>
    <label>Question</label><br><textarea name='q' required style='width:100%;padding:10px;margin:6px 0 14px 0;border-radius:8px;border:1px solid #ccc' rows='3'></textarea><br>
    <label>Answer</label><br><input name='a' required style='width:100%;padding:10px;margin:6px 0 14px 0;border-radius:8px;border:1px solid #ccc'><br>
    <label>Working</label><br><textarea name='work' style='width:100%;padding:10px;margin:6px 0 14px 0;border-radius:8px;border:1px solid #ccc' rows='3'></textarea><br>
    <button type='submit' style='padding:12px 24px;background:#0B1D51;color:white;border:none;border-radius:8px;font-weight:700'>Add Question</button>
    </form><br><a href='/admin'>Logout</a> | <a href='/'>Home</a></div></div>"""
