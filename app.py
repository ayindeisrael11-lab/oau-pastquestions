from flask import Flask
from flask import render_template_string

app = Flask(__name__)

past_questions = [
    {"course": "MTH 101", "year": "2022", "title": "Mathematics Past Question"},
    {"course": "PHY 101", "year": "2023", "title": "Physics Past Question"},
    {"course": "CHM 101", "year": "2021", "title": "Chemistry Past Question"},
]

HTML = """
<!DOCTYPE html>
<html>
<head><title>OAU Past Questions</title>
<style>
body{font-family: Arial; padding:20px; background:#f5f5f5}
.question-card{background:white; padding:15px; margin:10px; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1)}
#search{width:100%; padding:12px; font-size:16px; margin-bottom:20px}
</style>
</head>
<body>
<h1>OAU Past Questions is LIVE! 🎉</h1>
<input type="text" id="search" onkeyup="searchQ()" placeholder="Search courses...">
<div>
{% for q in questions %}
<div class="question-card">
<h3>{{ q.course }} - {{ q.year }}</h3>
<p>{{ q.title }}</p>
</div>
{% endfor %}
</div>
<script>
function searchQ() {
  var input = document.getElementById('search').value.toLowerCase();
  var cards = document.getElementsByClassName('question-card');
  for (var i=0; i<cards.length; i++) {
    if (cards[i].innerText.toLowerCase().includes(input)) {
      cards[i].style.display = "";
    } else {
      cards[i].style.display = "none";
    }
  }
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, questions=past_questions)

if __name__ == '__main__':
    app.run(debug=True)
