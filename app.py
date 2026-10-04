from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- DATABASE OF QUESTIONS ---
past_questions = [
    {
        "id": 1,
        "year": "2022/2023",
        "course": "PAD 101 - Intro to Public Administration",
        "question": "Define Public Administration and explain its scope.",
        "answer": "Public Administration is the implementation of government policy and also an academic discipline that studies this implementation.",
        "working": "1. Start with Woodrow Wilson's definition: government in action.\n2. Explain Scope: (a) Policy implementation, (b) Public bureaucracy, (c) Public management, (d) Inter-governmental relations, (e) Public interest.\n3. Give examples like Ministry, OAU registry as public administration."
    },
    {
        "id": 2,
        "year": "2022/2023",
        "course": "PAD 103 - Nigerian Government & Politics",
        "question": "Discuss the features of the 1999 Constitution of Nigeria.",
        "answer": "The 1999 Constitution is the supreme law of Nigeria operating a federal presidential system.",
        "working": "Features to explain: 1. Supremacy, 2. Federalism (Exclusive, Concurrent, Residual lists), 3. Presidential system, 4. Separation of Powers, 5. Fundamental Human Rights (Chapter 4), 6. Secularism. Conclude with its amendments."
    },
    {
        "id": 3,
        "year": "2021/2022",
        "course": "PAD 102 - Administrative Thought",
        "question": "Explain Max Weber's Bureaucratic Theory.",
        "answer": "Max Weber described bureaucracy as the most rational and efficient form of organization.",
        "working": "Explain 7 principles: 1. Division of Labour, 2. Hierarchy, 3. Formal Rules, 4. Impersonality, 5. Career Structure, 6. Formal Selection, 7. Written Documentation. Then add Criticisms: rigidity, red-tapism. Relate to OAU admin."
    }
]

# --- HTML TEMPLATE ---
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>OAU Public Admin Past Questions</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background: #f4f4f9; margin: 0; padding: 15px; }
       .header { background: #1a237e; color: white; padding: 20px; text-align: center; border-radius: 10px; }
       .card { background: white; padding: 20px; margin: 15px 0; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
       .year { background: #ffca28; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
       .course { color: #1a237e; font-weight: bold; margin-top: 10px; }
       .question { font-size: 18px; font-weight: bold; margin: 15px 0; }
       .btn { background: #1a237e; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
       .answer-box { background: #e8f5e9; padding: 15px; border-left: 5px solid green; margin-top: 15px; display: none; }
        input { width: 90%; padding: 12px; border-radius: 5px; border: 1px solid #ccc; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>OAU Past Questions</h1>
        <p>Public Administration - With Answers & Workings</p>
        <p style="font-size:13px;">Created by Israel</p>
        <input type="text" id="search" onkeyup="searchQ()" placeholder="Search e.g PAD 101, 2022, Constitution...">
    </div>

    {% for q in questions %}
    <div class="card question-card">
        <span class="year">{{ q.year }}</span>
        <div class="course">{{ q.course }}</div>
        <div class="question">{{ q.id }}. {{ q.question }}</div>
        <button class="btn" onclick="document.getElementById('ans{{ q.id }}').style.display='block'; this.style.display='none'">Show Answer & Working</button>
        <div class="answer-box" id="ans{{ q.id }}">
            <b>Answer:</b> {{ q.answer }} <br><br>
            <b>Working / How to answer:</b><br>
            <pre style="white-space: pre-wrap; font-family: Arial;">{{ q.working }}</pre>
        </div>
    </div>
    {% endfor %}

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
