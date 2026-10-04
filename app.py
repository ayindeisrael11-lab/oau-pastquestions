from flask import Flask, render_template_string, request, redirect, session, url_for
import json, os

app = Flask(__name__)
app.secret_key = "oau-great-ife-secret-2026"

FILE = "questions.json"
ADMIN_PASSWORD = "oau2026" # <--- YOUR ADMIN PASSWORD, change it!

# Load questions
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        past_questions = json.load(f)
else:
    past_questions = [
        {"id":1, "course":"MTH 101", "year":"2022", "title":"Elementary Mathematics I", "dept":"Mathematics"},
        {"id":2, "course":"PHY 101", "year":"2023", "title":"General Physics I", "dept":"Physics"},
        {"id":3, "course":"CHM 101", "year":"2021", "title":"General Chemistry I", "dept":"Chemistry"},
        {"id":4, "course":"CSC 101", "year":"2023", "title":"Introduction to Computing", "dept":"Computer Science"},
    ]
    with open(FILE, "w") as f:
        json.dump(past_questions, f)

def save():
    with open(FILE, "w") as f:
        json.dump(past_questions, f)

# ---------- PUBLIC SITE ----------
PUBLIC_HTML = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OAU Past Questions</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}body{font-family:Segoe UI,Arial;background:#f8f9ff;color:#333}
header{background:linear-gradient(135deg,#1a237e,#3949ab);color:white;padding:35px 20px;text-align:center}
header h1{font-size:30px}header p{opacity:.9;margin-top:8px}
.search-wrap{background:white;padding:18px;box-shadow:0 2px 10px rgba(0,0,0,.08);position:sticky;top:0;z-index:10}
#search{width:100%;max-width:600px;display:block;margin:0 auto;padding:14px 20px;border:2px solid #e0e0e0;border-radius:30px;outline:none;font-size:16px}
#search:focus{border-color:#3949ab}
.container{max-width:1100px;margin:25px auto;padding:0 15px;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.card{background:white;border-radius:16px;padding:22px;box-shadow:0 4px 15px rgba(0,0,0,.07);border-left:4px solid #3949ab;transition:.3s}
.card:hover{transform:translateY(-4px)}.badge{background:#e8eaf6;color:#1a237e;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:bold}
.card h3{margin:10px 0 5px;color:#1a237e}.card p{color:#666;font-size:14px;margin-bottom:15px}
.btn{display:block;text-align:center;background:#3949ab;color:white;padding:10px;border-radius:8px;text-decoration:none;font-weight:bold}
footer{text-align:center;padding:30px;color:#888;font-size:13px}
</style></head><body>
<header><h1>🎓 OAU Past Questions</h1><p>Obafemi Awolowo University - Ace your exams</p></header>
<div class="search-wrap"><input id="search" onkeyup="searchQ()" placeholder="🔍 Search MTH 101, PHY, 2023..."></div>
<div class="container" id="box">
{% for q in questions %}
<div class="card"><span class="badge">{{ q.dept }} • {{ q.year }}</span><h3>{{ q.course }}</h3><p>{{ q.title }}</p><a class="btn" href="#">View / Download</a></div>
{% endfor %}
</div>
<footer>Built for Great Ife Students | <a href="/admin">Admin Login</a><br>2026 - oau-pastquestions.onrender.com</footer>
<script>
function searchQ(){var v=document.getElementById('search').value.toLowerCase();var c=document.getElementsByClassName('card');for(var i=0;i<c.length;i++){c[i].style.display=c[i].innerText.toLowerCase().includes(v)?"":"none"}}
</script></body></html>
"""

# ---------- ADMIN LOGIN ----------
LOGIN_HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Admin Login</title>
<style>body{font-family:Arial;background:#f0f2ff;display:flex;justify-content:center;align-items:center;height:100vh}
.box{background:white;padding:30px;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.1);width:90%;max-width:350px}
input{width:100%;padding:12px;margin:10px 0;border:2px solid #ddd;border-radius:8px}
button{width:100%;padding:12px;background:#1a237e;color:white;border:none;border-radius:8px;font-weight:bold;cursor:pointer}
</style></head><body>
<div class="box"><h2>Admin Login</h2><p style="color:#666;font-size:14px">Enter password to manage questions</p>
<form method="POST"><input type="password" name="password" placeholder="Password" required><button>Login</button></form>
<p style="margin-top:15px;font-size:12px;color:#888">Default password: oau2026<br>Change it in app.py later</p></div></body></html>
"""

ADMIN_HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Admin Dashboard</title>
<style>body{font-family:Arial;background:#f8f9ff;padding:20px}.wrap{max-width:800px;margin:auto;background:white;padding:25px;border-radius:16px;box-shadow:0 4px 15px rgba(0,0,0,.08)}
input{width:100%;padding:10px;margin:6px 0;border:2px solid #ddd;border-radius:8px} button{padding:10px 18px;background:#1a237e;color:white;border:none;border-radius:8px;font-weight:bold;cursor:pointer}
table{width:100%;margin-top:20px;border-collapse:collapse} th,td{padding:10px;border-bottom:1px solid #eee;text-align:left;font-size:14px} a.del{color:red;text-decoration:none;font-weight:bold}
.top{display:flex;justify-content:space-between;align-items:center}
</style></head><body>
<div class="wrap">
<div class="top"><h2>Admin Dashboard</h2><a href="/logout">Logout</a></div>
<p style="color:#666">Add new past question - it will appear live instantly!</p>
<form method="POST" action="/add">
<input name="course" placeholder="Course Code e.g MTH 201" required>
<input name="year" placeholder="Year e.g 2023" required>
<input name="title" placeholder="Title e.g Engineering Mathematics" required>
<input name="dept" placeholder="Department e.g Mathematics" required>
<button type="submit">+ Add Question</button>
</form>
<table><tr><th>Course</th><th>Year</th><th>Title</th><th>Action</th></tr>
{% for q in questions %}
<tr><td>{{ q.course }}</td><td>{{ q.year }}</td><td>{{ q.title }}</td><td><a class="del" href="/delete/{{ q.id }}">Delete</a></td></tr>
{% endfor %}
</table>
<br><a href="/">← View Public Website</a>
</div></body></html>
"""

@app.route('/')
def home():
    return render_template_string(PUBLIC_HTML, questions=past_questions)

@app.route('/admin', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/dashboard')
        else:
            return "Wrong password! <a href='/admin'>Try again</a>"
    return render_template_string(LOGIN_HTML)

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')
    return render_template_string(ADMIN_HTML, questions=past_questions)

@app.route('/add', methods=['POST'])
def add_q():
    if not session.get('admin'):
        return redirect('/admin')
    new_id = max([q['id'] for q in past_questions], default=0) + 1
    past_questions.append({
        "id": new_id,
        "course": request.form['course'],
        "year": request.form['year'],
        "title": request.form['title'],
        "dept": request.form['dept']
    })
    save()
    return redirect('/dashboard')

@app.route('/delete/<int:qid>')
def delete_q(qid):
    if not session.get('admin'):
        return redirect('/admin')
    global past_questions
    past_questions = [q for q in past_questions if q['id']!= qid]
    save()
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
