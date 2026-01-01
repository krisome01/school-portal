import logging
import os
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
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
    "student2": {"password": "password123", "role": "student", "avatar": "student2.png", "house": "blue", "badge": "None", "high_score": 0},
"student3": {"password": "password123", "role": "student", "avatar": "student3.png", "house": "green", "badge": "None", "high_score": 0},
"student4": {"password": "password123", "role": "student", "avatar": "student4.png", "house": "yellow", "badge": "None", "high_score": 0},
"student5": {"password": "password123", "role": "student", "avatar": "student5.png", "house": "red", "badge": "None", "high_score": 0},
"student6": {"password": "password123", "role": "student", "avatar": "student6.png", "house": "blue", "badge": "None", "high_score": 0},
"student7": {"password": "password123", "role": "student", "avatar": "student7.png", "house": "green", "badge": "None", "high_score": 0},
"student8": {"password": "password123", "role": "student", "avatar": "student8.png", "house": "yellow", "badge": "None", "high_score": 0},
"student9": {"password": "password123", "role": "student", "avatar": "student9.png", "house": "red", "badge": "None", "high_score": 0},
"student10": {"password": "password123", "role": "student", "avatar": "student10.png", "house": "blue", "badge": "None", "high_score": 0},
"student11": {"password": "password123", "role": "student", "avatar": "student11.png", "house": "green", "badge": "None", "high_score": 0},
"student12": {"password": "password123", "role": "student", "avatar": "student12.png", "house": "yellow", "badge": "None", "high_score": 0},
"student13": {"password": "password123", "role": "student", "avatar": "student13.png", "house": "red", "badge": "None", "high_score": 0},
"student14": {"password": "password123", "role": "student", "avatar": "student14.png", "house": "blue", "badge": "None", "high_score": 0},
"student15": {"password": "password123", "role": "student", "avatar": "student15.png", "house": "green", "badge": "None", "high_score": 0},
"student16": {"password": "password123", "role": "student", "avatar": "student16.png", "house": "yellow", "badge": "None", "high_score": 0},
"student17": {"password": "password123", "role": "student", "avatar": "student17.png", "house": "red", "badge": "None", "high_score": 0},
"student18": {"password": "password123", "role": "student", "avatar": "student18.png", "house": "blue", "badge": "None", "high_score": 0},
"student19": {"password": "password123", "role": "student", "avatar": "student19.png", "house": "green", "badge": "None", "high_score": 0},
"student20": {"password": "password123", "role": "student", "avatar": "student20.png", "house": "yellow", "badge": "None", "high_score": 0},
"student21": {"password": "password123", "role": "student", "avatar": "student21.png", "house": "red", "badge": "None", "high_score": 0},
"student22": {"password": "password123", "role": "student", "avatar": "student22.png", "house": "blue", "badge": "None", "high_score": 0},
"student23": {"password": "password123", "role": "student", "avatar": "student23.png", "house": "green", "badge": "None", "high_score": 0},
"student24": {"password": "password123", "role": "student", "avatar": "student24.png", "house": "yellow", "badge": "None", "high_score": 0},
"student25": {"password": "password123", "role": "student", "avatar": "student25.png", "house": "red", "badge": "None", "high_score": 0},
"student26": {"password": "password123", "role": "student", "avatar": "student26.png", "house": "blue", "badge": "None", "high_score": 0},
"student27": {"password": "password123", "role": "student", "avatar": "student27.png", "house": "green", "badge": "None", "high_score": 0},
"student28": {"password": "password123", "role": "student", "avatar": "student28.png", "house": "yellow", "badge": "None", "high_score": 0},
"student29": {"password": "password123", "role": "student", "avatar": "student29.png", "house": "red", "badge": "None", "high_score": 0},
"student30": {"password": "password123", "role": "student", "avatar": "student30.png", "house": "blue", "badge": "None", "high_score": 0},
"student31": {"password": "password123", "role": "student", "avatar": "student31.png", "house": "green", "badge": "None", "high_score": 0},
"student32": {"password": "password123", "role": "student", "avatar": "student32.png", "house": "yellow", "badge": "None", "high_score": 0},
"student33": {"password": "password123", "role": "student", "avatar": "student33.png", "house": "red", "badge": "None", "high_score": 0},
"student34": {"password": "password123", "role": "student", "avatar": "student34.png", "house": "blue", "badge": "None", "high_score": 0},
"student35": {"password": "password123", "role": "student", "avatar": "student35.png", "house": "green", "badge": "None", "high_score": 0},
"student36": {"password": "password123", "role": "student", "avatar": "student36.png", "house": "yellow", "badge": "None", "high_score": 0},
"student37": {"password": "password123", "role": "student", "avatar": "student37.png", "house": "red", "badge": "None", "high_score": 0},
"student38": {"password": "password123", "role": "student", "avatar": "student38.png", "house": "blue", "badge": "None", "high_score": 0},
"student39": {"password": "password123", "role": "student", "avatar": "student39.png", "house": "green", "badge": "None", "high_score": 0},
"student40": {"password": "password123", "role": "student", "avatar": "student40.png", "house": "yellow", "badge": "None", "high_score": 0},
"student41": {"password": "password123", "role": "student", "avatar": "student41.png", "house": "red", "badge": "None", "high_score": 0},
"student42": {"password": "password123", "role": "student", "avatar": "student42.png", "house": "blue", "badge": "None", "high_score": 0},
"student43": {"password": "password123", "role": "student", "avatar": "student43.png", "house": "green", "badge": "None", "high_score": 0},
"student44": {"password": "password123", "role": "student", "avatar": "student44.png", "house": "yellow", "badge": "None", "high_score": 0},
    "teacher": {
        "password": "teach2025",
        "role": "teacher",
        "avatar": "teacher.png",
        "house": "yellow",
        "badge": "None",
        "high_score": 0
    }
    "teacher2": {"password": "teach2025", "role": "teacher", "avatar": "teacher2.png", "house": "blue", "badge": "None", "high_score": 0},
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
import os
import logging

logging.basicConfig(level=logging.INFO)

@app.route("/dashboard/<username>/<role>/<avatar>")
def dashboard(username, role, avatar):
    logging.info(f"Dashboard accessed by {username} with avatar {avatar}")

    if username not in users:
        logging.error(f"User '{username}' not found in users dictionary")
        return "User not found", 404

    user = users.get(username)

    if not user:
        logging.error(f"User '{username}' not found in users dictionary")
        return "User not found", 404

    # Guarantee required fields exist
    user.setdefault("house", "red")
    user.setdefault("badge", "None")
    user.setdefault("high_score", 0)

    # Use absolute path for avatar check
    static_folder = os.path.join(os.path.dirname(__file__), "static")
    avatar_path = avatar if os.path.exists(os.path.join(static_folder, avatar)) else "default.png"

    if avatar_path == "default.png":
        logging.warning(f"Avatar file missing: {avatar}. Using default.png instead.")

    house_points = {"red": 0, "blue": 0, "green": 0, "yellow": 0}
    for username_key, data in users.items():
        house = data.get("house") or "red"
        house_points[house] += data.get("high_score", 0)

    house_of_week = max(house_points, key=house_points.get)

    house_mottos = {
        "red": "Courage, creativity, and heart.",
        "blue": "Wisdom, curiosity, and calm.",
        "green": "Ambition, resilience, and growth.",
        "yellow": "Kindness, loyalty, and joy."
    }

    logging.info(
        f"DEBUG: user={user}, avatar_path={avatar_path}, "
        f"house_points={house_points}, house_of_week={house_of_week}"
    )

    try:
        return render_template(
            "dashboard.html",
            username=username,
            role=role,
            avatar=avatar_path,
            user=user,
            house_points=house_points,
            house_of_week=house_of_week,
            house_mottos=house_mottos
        )
    except Exception as e:
        logging.error(f"Dashboard render failed: {e}")
        return "Dashboard crashed", 500

# -----------------------------
# PROFILE PAGE
# -----------------------------
@app.route("/profile/<username>/<role>/<avatar>")
def profile(username, role, avatar):
    user = users.get(username)

    if not user:
        logging.error(f"User '{username}' not found in users dictionary")
        return "User not found", 404

    return render_template("profile.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           user=user)

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
@app.route("/create-student/<username>/<role>/<avatar>", methods=["GET", "POST"])
def create_student(username, role, avatar):
    # Only teachers can create students
    if role != "teacher":
        return "Access denied", 403

    message = ""

    if request.method == "POST":
        new_username = request.form["username"].strip()
        password = request.form["password"].strip()
        house = request.form["house"]

        # Check if username already exists
        if new_username in users:
            message = "That username already exists. Try another one."
        else:
            # Create avatar filename automatically
            avatar_filename = f"{new_username}.png"

            # Add new student to users dictionary
            users[new_username] = {
                "password": password,
                "role": "student",
                "avatar": avatar_filename,
                "house": house,
                "badge": "None",
                "high_score": 0
            }

            logging.info(f"New student created: {new_username}")

            return redirect(url_for("dashboard",
                                    username=username,
                                    role=role,
                                    avatar=avatar))

    return render_template("create_student.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           message=message)
@app.route("/view-students/<username>/<role>/<avatar>")
def view_students(username, role, avatar):
    if role != "teacher":
        return "Access denied", 403

    student_list = []
    for user_key, data in users.items():
        if data.get("role") == "student":
            student_list.append({
                "username": user_key,
                "avatar": data.get("avatar", "default.png"),
                "house": data.get("house", "red"),
                "badge": data.get("badge", "None"),
                "high_score": data.get("high_score", 0)
            })

    student_list.sort(key=lambda x: x["username"])

    return render_template("view_students.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           students=student_list)
 @app.route("/student/<username>/<role>/<avatar>/<student_username>")
def view_student(username, role, avatar, student_username):
    # Only teachers can view student profiles
    if role != "teacher":
        return "Access denied", 403

    student = users.get(student_username)
    if not student:
        return "Student not found", 404

    return render_template("view_student.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           student_username=student_username,
                           student=student)   
# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run()
















