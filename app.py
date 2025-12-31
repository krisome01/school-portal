import os
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

# -----------------------------
# USER DATA
# -----------------------------
users = {
    "student1": {
        "password": "password123",
        "role": "student",
        "avatar": "student1.png",
        "house": "red",
        "badge": "None",
        "high_score": 0
    },
    "teacher": {
        "password": "teach2025",
        "role": "teacher",
        "avatar": "teacher.png",
        "badge": "None",
        "high_score": 0
    }
}

# -----------------------------
# QUIZ QUESTIONS
# -----------------------------
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

# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)

        if user and user["password"] == password:
            return redirect(url_for("dashboard",
                                    username=username,
                                    role=user["role"],
                                    avatar=user["avatar"]))
        else:
            message = "Oops! That username or password didn't match. Try again?"

    return render_template("login.html", message=message)

# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/dashboard/<username>/<role>/<avatar>")
def dashboard(username, role, avatar):

    # Calculate house points
    house_points = {"red": 0, "blue": 0, "green": 0, "yellow": 0}
    for user, data in users.items():
        house = data.get("house")
        house_points[house] += data.get("high_score", 0)

    # Determine house of the week
    house_of_week = max(house_points, key=house_points.get)

    # House mottos
    house_mottos = {
        "red": "Courage, creativity, and heart.",
        "blue": "Wisdom, curiosity, and calm.",
        "green": "Ambition, resilience, and growth.",
        "yellow": "Kindness, loyalty, and joy."
    }

    return render_template(
        "dashboard.html",
        username=username,
        role=role,
        avatar=avatar,
        user=users[username],
        house_points=house_points,
        house_of_week=house_of_week,
        house_mottos=house_mottos
    )

# -----------------------------
# PROFILE PAGE
# -----------------------------
@app.route("/profile/<username>/<role>/<avatar>")
def profile(username, role, avatar):
    return render_template("profile.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           user=users[username])

# -----------------------------
# QUIZ GAME
# -----------------------------
@app.route("/quiz/<username>/<role>/<avatar>", methods=["GET", "POST"])
def quiz(username, role, avatar):
    if "quiz_index" not in session:
        session["quiz_index"] = 0
        session["score"] = 0
        shuffled = quiz_questions.copy()
        random.shuffle(shuffled)
        session["quiz_order"] = shuffled

    index = session["quiz_index"]
    score = session["score"]

    if index >= len(session["quiz_order"]):
        final_score = score

        # Award badge
        if final_score == 3:
            users[username]["badge"] = "Gold"
        elif final_score == 2:
            users[username]["badge"] = "Silver"
        elif final_score == 1:
            users[username]["badge"] = "Bronze"
        else:
            users[username]["badge"] = "None"

        # Update high score
        if final_score > users[username]["high_score"]:
            users[username]["high_score"] = final_score

        # Reset session
        session.pop("quiz_index")
        session.pop("score")
        session.pop("quiz_order")

        return render_template("quiz_result.html",
                               score=final_score,
                               username=username,
                               role=role,
                               avatar=avatar)

    question = session["quiz_order"][index]
    message = ""

    if request.method == "POST":
        user_answer = request.form["answer"]
        if user_answer == question["answer"]:
            session["score"] += 1
        session["quiz_index"] += 1
        return redirect(url_for("quiz", username=username, role=role, avatar=avatar))

    return render_template("quiz.html",
                           question=question,
                           message=message,
                           username=username,
                           role=role,
                           avatar=avatar)

# -----------------------------
# LEADERBOARD
# -----------------------------
@app.route("/leaderboard/<username>/<role>/<avatar>")
def leaderboard(username, role, avatar):
    leaderboard_data = []
    for user, data in users.items():
        leaderboard_data.append({
            "username": user,
            "badge": data.get("badge", "None"),
            "high_score": data.get("high_score", 0),
            "avatar": data.get("avatar", "default.png"),
            "house": data.get("house", "red")
        })

    leaderboard_data.sort(key=lambda x: x["high_score"], reverse=True)

    return render_template("leaderboard.html",
                           leaderboard=leaderboard_data,
                           username=username,
                           role=role,
                           avatar=avatar)

# -----------------------------
# PLACEHOLDER PAGES
# -----------------------------
@app.route("/announcements/<username>/<role>/<avatar>")
def announcements(username, role, avatar):
    return render_template("announcements.html",
                           username=username, role=role, avatar=avatar)

@app.route("/grades/<username>/<role>/<avatar>")
def grades(username, role, avatar):
    return render_template("grades.html",
                           username=username, role=role, avatar=avatar)

@app.route("/upload-homework/<username>/<role>/<avatar>")
def upload_homework(username, role, avatar):
    return render_template("upload_homework.html",
                           username=username, role=role, avatar=avatar)

@app.route("/add-announcement/<username>/<role>/<avatar>")
def add_announcement(username, role, avatar):
    return render_template("add_announcement.html",
                           username=username, role=role, avatar=avatar)

@app.route("/add-grade/<username>/<role>/<avatar>")
def add_grade(username, role, avatar):
    return render_template("add_grade.html",
                           username=username, role=role, avatar=avatar)

@app.route("/calendar/<username>/<role>/<avatar>")
def calendar_page(username, role, avatar):
    return render_template("calendar.html",
                           username=username, role=role, avatar=avatar)

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
