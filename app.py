from flask import Flask, render_template_string, request, redirect
import os, requests

app = Flask(__name__)

PAYSTACK_PUBLIC_KEY = os.environ.get("PAYSTACK_PUBLIC_KEY", "pk_test_12852a55b3989f96627a656eb530538a7c7530ec")
PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY", "sk_test_87f32cc736b3b0015e5e989352e8f1435b7bef3b")

COURSES = {
    "MTH101": {"name": "Elementary Mathematics I", "dept": "All Science", "price": 500},
    "CHM101": {"name": "Introductory Chemistry I", "dept": "Science", "price": 500},
    "PHY101": {"name": "Introductory Physics I", "dept": "Science", "price": 500},
    "BIO101": {"name": "Introductory Biology I", "dept": "Science", "price": 500},
    "CSC101": {"name": "Introduction to Computing", "dept": "All Faculties", "price": 300},
    "OAU-POST-UTME": {"name": "OAU Post-UTME Past Questions (All Subjects)", "dept": "Aspirants", "price": 1000},
}

QUESTIONS_DB = {
    "MTH101": [
        {"q": "Find limit of (x²-1)/(x-1) as x->1", "a": "2", "year": "2023", "work": "Factorize: (x-1)(x+1)/(x-1) = x+1 = 2"},
        {"q": "Differentiate y = 3x³ + 2x", "a": "9x² + 2", "year": "2022", "work": "Use power rule"},
        {"q": "Solve: 2x + 3 = 7", "a": "x=2", "year": "2023", "work": "2x=4, x=2"},
        {"q": "Integrate x² dx", "a": "x³/3 + C", "year": "2021", "work": "Power rule for integration"},
        {"q": "What is 20% of 150?", "a": "30", "year": "2024", "work": "0.2*150"},
    ],
    "CHM101": [
        {"q": "What is Avogadro's number?", "a": "6.02 x 10^23", "year": "2023", "work": "Constant"},
        {"q": "Define Isotope", "a": "Same protons, different neutrons", "year": "2022", "work": "Example: C-12 and C-14"},
    ]
}

HOME_HTML = """
<!DOCTYPE html><html><head><title>OAU Past Questions</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:Arial;max-width:900px;margin:auto;padding:20px;background:#f5f5f5}
.card{background:white;padding:15px;margin:10px 0;border-radius:10px;box-shadow:0 2px 5px #ccc}
.btn{background:#003366;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;display:inline-block}
.price{color:green;font-weight:bold}</style></head><body>
<h1>🎓 OAU Past Questions Hub</h1><p>Original OAU Past Questions 2019-2024 | Paystack Secured</p>
{% for code, info in courses.items() %}
<div class="card"><h3>{{code}} - {{info.name}}</h3><p>Dept: {{info.dept}}</p>
<p class="price">₦{{info.price}} - Full Pack</p><a class="btn" href="/course/{{code}}">View Free Preview</a></div>
{% endfor %}</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_HTML, courses=COURSES)

@app.route('/course/<code>')
def course_page(code):
    course = COURSES.get(code)
    if not course: return "Course not found"
    qs = QUESTIONS_DB.get(code, [{"q":"Real questions loading... Contact admin","a":"-","year":"2024","work":"Coming soon"}])
    html = f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://js.paystack.co/v1/inline.js"></script>
    <style>body{{font-family:Arial;max-width:800px;margin:auto;padding:20px}} .q{{background:#fff;padding:15px;margin:10px 0;border-left:4px solid #003366}}</style></head><body>
    <a href="/">← Back</a><h1>{code} - {course['name']}</h1>
    <p>Showing 2 free. Pay ₦{course['price']} to unlock all</p>
    """
    for q in qs[:2]:
        html += f"<div class='q'><b>{q['year']}</b><br>{q['q']}<br><i>Ans: {q['a']}<br>Working: {q['work']}</i></div>"
    html += f"""
    <div style="background:#fff3cd;padding:20px;text-align:center;margin-top:20px;border-radius:10px">
    <h2>Unlock Full Pack - ₦{course['price']}</h2>
    <input id="email" placeholder="Enter your email" style="padding:12px;width:80%;margin-bottom:10px;border-radius:5px;border:1px solid #ccc"><br>
    <button onclick="payWithPaystack()" style="padding:15px 30px;background:green;color:white;border:none;border-radius:10px;font-size:18px">Pay Now with Paystack</button>
    <p>Secured by Paystack - Test card: 4084 0840 8408 4081</p>
    </div>
    <script>
    function payWithPaystack(){{
      var email = document.getElementById('email').value;
      if(!email){{ alert('Please enter email'); return; }}
      var handler = PaystackPop.setup({{
        key: '{PAYSTACK_PUBLIC_KEY}',
        email: email,
        amount: {course['price']} * 100,
        currency: 'NGN',
        ref: 'OAU_'+Math.floor((Math.random() * 1000000000) + 1),
        callback: function(response){{ window.location.href = "/verify/{code}/" + response.reference + "?email=" + email; }},
        onClose: function(){{ alert('Payment window closed'); }}
      }});
      handler.openIframe();
    }}
    </script></body></html>
    """
    return html

@app.route('/verify/<code>/<ref>')
def verify(code, ref):
    email = request.args.get('email', 'student@oau.com')
    course = COURSES.get(code)
    # Verify with Paystack
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    r = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
    data = r.json()
    if data.get('status') and data['data']['status'] == 'success':
        qs = QUESTIONS_DB.get(code, [])
        html = f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1'><style>body{{font-family:Arial;max-width:800px;margin:auto;padding:20px}} .q{{background:#fff;padding:15px;margin:10px 0;border-left:4px solid green}}</style></head><body>"
        html += f"<h1 style='color:green'>✅ Payment Successful!</h1><p>Reference: {ref}</p><h2>{code} - Full Pack Unlocked</h2>"
        for q in qs:
            html += f"<div class='q'><b>{q['year']}</b> - {q['q']}<br><b>Ans:</b> {q['a']}<br><b>Working:</b> {q['work']}</div>"
        html += "<br><a href='/' style='background:#003366;color:white;padding:10px 20px;border-radius:5px;text-decoration:none'>Back to Home</a></body></html>"
        return html
    else:
        return f"Payment verification failed. Ref: {ref} <br><a href='/course/{code}'>Try again</a>"

if __name__ == '__main__':
    app.run()
