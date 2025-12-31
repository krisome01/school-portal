import json
import os
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "png", "jpg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = {
    "student1": {
        "password": "password123",
        "role": "student",
        "avatar": "student1.png"
    },
    "teacher": {
        "password": "teach2025",
        "role": "teacher",
        "avatar": "teacher.png"
    }
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["user"]
        password = request.form["password"]

        # Check credentials, redirect to dashboard
        # Or show error message

    return render_template("login.html")

@app.route("/dashboard/<username>/<role>/<avatar>")
def dashboard(username, role, avatar):
    return render_template("dashboard.html", username=username, role=role, avatar=avatar)

announcements_list = [
    {"date": "January 6", "emoji": "📅", "text": "School reopens"},
    {"date": "February 12", "emoji": "📝", "text": "Mock exams start"},
    {"date": "March 3", "emoji": "👨‍👩‍👧", "text": "Year 7 Parents Evening"}
]

@app.route("/announcements/<username>/<role>/<avatar>", methods=["GET", "POST"])
def announcements(username, role, avatar):
    if request.method == "POST":
        date = request.form["date"]
        emoji = request.form["emoji"]
        text = request.form["text"]

        announcements_list.append({
            "date": date,
            "emoji": emoji,
            "text": text
        })

    return render_template(
        "announcements.html",
        announcements=announcements_list,
        title="Announcements",
        username=username,
        role=role,
        avatar=avatar
    )

@app.route("/grades/<username>/<role>/<avatar>")
def grades(username, role, avatar):
    return render_template("grades.html", title="Grades", username=username, role=role, avatar=avatar)

@app.route("/profile/<username>/<role>/<avatar>")
def profile(username, role, avatar):
    return render_template("profile.html", username=username, role=role, avatar=avatar)

@app.route("/logout")
def logout():
    return redirect(url_for("home"))

@app.route("/choose-avatar/<username>/<role>/<avatar>")
def choose_avatar(username, role, avatar):
    avatars = [
        "student1.png",
        "student2.png",
        "student3.png",
        "teacher1.png",
        "teacher2.png"
    ]
    return render_template("choose_avatar.html", avatars=avatars, username=username, role=role, avatar=avatar)

@app.route("/set-avatar/<username>/<role>/<new_avatar>")
def set_avatar(username, role, new_avatar):
    users[username]["avatar"] = new_avatar
    return redirect(f"/profile/{username}/{role}/{new_avatar}")

@app.route("/calendar/<username>/<role>/<avatar>")
def calendar(username, role, avatar):
    calendar_days = []

    # Create 31 days for January
    for i in range(1, 32):
        day_str = f"January {i}"
        events = [a for a in announcements_list if a["date"] == day_str]
        calendar_days.append({"day": i, "events": events})

    return render_template("calendar.html", calendar_days=calendar_days, username=username, role=role, avatar=avatar)

@app.route("/upload-homework/<username>/<role>/<avatar>", methods=["GET", "POST"])
def upload_homework(username, role, avatar):
    message = ""

    if role != "student":
        return "Access denied", 403

    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{username}_{file.filename}")
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            message = "Homework uploaded successfully!"

    return render_template("upload_homework.html",
                           username=username, role=role, avatar=avatar,
                           message=message)
    quiz_questions = [
    {
        "text": "What is 5 + 7?",
        "options": ["10", "11", "12", "13"],
        "answer": "12"
    }
]
quiz_questions = [
    {
        "text": "What is 5 + 7?",
        "options": ["10", "11", "12", "13"],
        "answer": "12"
    },
    {
        "text": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
    },
    {
        "text": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
    }
]

@app.route("/quiz/<username>/<role>/<avatar>", methods=["GET", "POST"])
def quiz(username, role, avatar):
    if "quiz_index" not in session:
        session["quiz_index"] = 0
        session["score"] = 0

    index = session["quiz_index"]
    score = session["score"]
    message = ""

    if index >= len(quiz_questions):
        final_score = score
        session.pop("quiz_index")
        session.pop("score")
        return render_template("quiz_result.html", score=final_score,
                               username=username, role=role, avatar=avatar)

    question = quiz_questions[index]

    if request.method == "POST":
        user_answer = request.form["answer"]
        if user_answer == question["answer"]:
            session["score"] += 1
            message = "Correct! 🎉"
        else:
            message = "Oops, try again!"

        session["quiz_index"] += 1
        return redirect(url_for("quiz", username=username, role=role, avatar=avatar))

    return render_template("quiz.html", question=question, message=message,
                           username=username, role=role, avatar=avatar)

    
# REMOVE app.run() — Render will run the app using gunicorn
















