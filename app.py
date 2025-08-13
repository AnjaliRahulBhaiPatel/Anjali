from flask import Flask, render_template, request
import os
import PyPDF2
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'resume_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

KEYWORDS = {
    'Python': 'Software Developer',
    'Machine Learning': 'Data Scientist',
    'Leadership': 'Project Manager',
    'Teamwork': 'HR Specialist',
    'JavaScript': 'Frontend Developer'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()

    found = [kw for kw in KEYWORDS if kw.lower() in text.lower()]
    missing = [kw for kw in KEYWORDS if kw.lower() not in text.lower()]
    score = len(found) / len(KEYWORDS) * 100

    suggestions = [KEYWORDS[k] for k in found]
    improvements = []
    if not re.search(r'\bemail\b|\b@\b', text.lower()):
        improvements.append("Add your email address")
    if "education" not in text.lower():
        improvements.append("Include your education section")
    if "experience" not in text.lower():
        improvements.append("Add your work experience")
    if len(text.split()) > 1000:
        improvements.append("Consider shortening your resume")

    return render_template('index.html',
        uploaded=True,
        found=found,
        missing=missing,
        score=round(score, 1),
        suggestions=suggestions,
        improvements=improvements
    )

if __name__ == '__main__':
    app.run(debug=True)
