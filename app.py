from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

skills_list = [
    "Python",
    "Java",
    "C++",
    "Machine Learning",
    "Flask",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
    "TensorFlow",
    "AI"
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    file = request.files['resume']

    if file:

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            file.filename
        )

        file.save(filepath)

        text = ""

        try:

            pdf = PdfReader(filepath)

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted

        except:
            return "Invalid or Corrupted PDF File ❌"

        # Skills Detection

        found_skills = []
        missing_skills = []

        for skill in skills_list:

            if skill.lower() in text.lower():
                found_skills.append(skill)

            else:
                missing_skills.append(skill)

        # ATS Score

        ats_score = len(found_skills) * 10

        if ats_score > 100:
            ats_score = 100

        # Predicted Role

        predicted_role = "General"

        if "machine learning" in text.lower() or "tensorflow" in text.lower():
            predicted_role = "AI/ML Engineer"

        elif "html" in text.lower() and "css" in text.lower():
            predicted_role = "Web Developer"

        elif "sql" in text.lower():
            predicted_role = "Data Analyst"

        elif "java" in text.lower():
            predicted_role = "Java Developer"

        # Resume Strength

        if ats_score >= 80:
            level = "Excellent Resume 🚀"

        elif ats_score >= 50:
            level = "Good Resume 👍"

        else:
            level = "Needs Improvement ⚠️"

        # Suggestions

        suggestions = []

        if "projects" not in text.lower():
            suggestions.append("Add Projects Section")

        if "internship" not in text.lower():
            suggestions.append("Add Internship Experience")

        if ats_score < 50:
            suggestions.append("Add More Technical Skills")

        if "github" not in text.lower():
            suggestions.append("Add GitHub Profile")

        if "linkedin" not in text.lower():
            suggestions.append("Add LinkedIn Profile")

        # AI Interview Questions

        interview_questions = []

        if "python" in text.lower():
            interview_questions.append(
                "Explain the difference between List and Tuple in Python."
            )

        if "machine learning" in text.lower():
            interview_questions.append(
                "Explain supervised vs unsupervised learning."
            )

        if "html" in text.lower():
            interview_questions.append(
                "What is the difference between HTML and HTML5?"
            )

        if "sql" in text.lower():
            interview_questions.append(
                "What is the difference between DELETE and TRUNCATE?"
            )

        if "java" in text.lower():
            interview_questions.append(
                "Explain OOP concepts in Java."
            )

        if len(interview_questions) == 0:
            interview_questions.append(
                "Tell me about yourself."
            )

        return render_template(
            'result.html',
            skills=found_skills,
            missing=missing_skills,
            score=ats_score,
            suggestions=suggestions,
            predicted_role=predicted_role,
            level=level,
            interview_questions=interview_questions
        )

    return "No File Uploaded ❌"


if __name__ == '__main__':
    app.run(debug=True)