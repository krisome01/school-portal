from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
import json
import os

def load_json(filename):
    path = os.path.join("data", filename)
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(filename, data):
    path = os.path.join("data", filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------------------
# Teacher Accounts
# -----------------------------------

users = {}

users["missomeata"] = {
    "password": "teach2025",
    "role": "teacher",
    "avatar": "teacher.png",
    "display_name": "Miss Omeata"
}

users["mromeata"] = {
    "password": "teach2025",
    "role": "teacher",
    "avatar": "teacher1.png",
    "display_name": "Mr Omeata"
}

# -----------------------------------
# Student Names (ClassDojo)
# -----------------------------------

student_names = [
    "Amelia", "Amy", "Ana", "Bar", "Barrie", "Barrington", "Barry", "Blueberry",
    "Charlotte", "Chealsea", "Chen", "Choco", "Daisy", "Dakota", "Gissele", "Hally",
    "Harriete", "Hope", "Iggle", "Jakella", "Linus", "Lowe", "Masha", "Maya",
    "Mina", "Oaty", "Octar", "Octo", "Otto", "Po", "Poppy", "Rocket", "Rosetta",
    "Scarlett", "Scot", "Squirtle", "Susan", "Susie", "Sylvia", "Tatiana", "Upsy",
    "Vanilla", "Violet", "Zed"
]

student_avatars = ["student1.png", "student2.png", "student3.png"]
houses = ["red", "blue", "green", "yellow"]

# -----------------------------------
# Auto-generate 44 Students
# -----------------------------------

for idx, name in enumerate(student_names):
    username = f"student{idx + 1}"
    avatar = student_avatars[idx % len(student_avatars)]
    house = houses[idx % len(houses)]

    users[username] = {
        "password": "password123",
        "role": "student",
        "avatar": avatar,
        "house": house,
        "badge": "None",
        "high_score": 0,
        "notes": [],
        "progress": [],
        "attendance": [],
        "display_name": name,
        "house_points": 0,
        "behaviour_points": []
    }

# -----------------------------------
# Helper
# -----------------------------------

def today_str():
    return datetime.now().strftime("%Y-%m-%d")

# -----------------------------------
# Login
# -----------------------------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = users.get(username)
        if user and user["password"] == password:
            return redirect(url_for(
                "dashboard",
                username=username,
                role=user["role"],
                avatar=user["avatar"]
            ))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# -----------------------------------
# Dashboard
# -----------------------------------

@app.route("/dashboard/<username>/<role>/<avatar>")
def dashboard(username, role, avatar):
    user = users.get(username)
    return render_template("dashboard.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           user=user)

# -----------------------------------
# Profile
# -----------------------------------

@app.route("/profile/<username>/<role>/<avatar>")
def profile(username, role, avatar):
    user = users.get(username)
    return render_template("profile.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           user=user)

# -----------------------------------
# View All Students
# -----------------------------------

@app.route("/view-students/<username>/<role>/<avatar>")
def view_students(username, role, avatar):
    if role != "teacher":
        return "Access denied", 403

    student_list = []
    for uname, data in users.items():
        if data["role"] == "student":
            student_list.append({
                "username": uname,
                "display_name": data["display_name"],
                "avatar": data["avatar"],
                "house": data["house"],
                "badge": data["badge"],
                "high_score": data["high_score"],
                "house_points": data["house_points"]
            })

    student_list.sort(key=lambda x: x["display_name"])

    return render_template("view_students.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           students=student_list)

# -----------------------------------
# View Single Student
# -----------------------------------

@app.route("/student/<username>/<role>/<avatar>/<student_username>")
def view_student(username, role, avatar, student_username):
    if role != "teacher":
        return "Access denied", 403

    student = users.get(student_username)
    return render_template("view_student.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           student_username=student_username,
                           student=student)

# -----------------------------------
# Edit Student
# -----------------------------------

@app.route("/edit-student/<username>/<role>/<avatar>/<student_username>",
           methods=["GET", "POST"])
def edit_student(username, role, avatar, student_username):
    if role != "teacher":
        return "Access denied", 403

    student = users.get(student_username)

    if request.method == "POST":
        student["password"] = request.form["password"]
        student["house"] = request.form["house"]
        student["badge"] = request.form["badge"]

        hs = request.form.get("high_score")
        if hs.isdigit():
            student["high_score"] = int(hs)

        return redirect(url_for("view_student",
                                username=username,
                                role=role,
                                avatar=avatar,
                                student_username=student_username))

    return render_template("edit_student.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           student_username=student_username,
                           student=student)

# -----------------------------------
# Delete Student
# -----------------------------------

@app.route("/delete-student/<username>/<role>/<avatar>/<student_username>")
def delete_student(username, role, avatar, student_username):
    if role != "teacher":
        return "Access denied", 403

    if student_username in users:
        del users[student_username]

    return redirect(url_for("view_students",
                            username=username,
                            role=role,
                            avatar=avatar))

# -----------------------------------
# Add Note
# -----------------------------------

@app.route("/add-note/<username>/<role>/<avatar>/<student_username>",
           methods=["POST"])
def add_note(username, role, avatar, student_username):
    if role != "teacher":
        return "Access denied", 403

    note = request.form.get("note")
    users[student_username]["notes"].append(note)

    return redirect(url_for("view_student",
                            username=username,
                            role=role,
                            avatar=avatar,
                            student_username=student_username))

# -----------------------------------
# Add Score
# -----------------------------------

@app.route("/add-score/<username>/<role>/<avatar>/<student_username>",
           methods=["POST"])
def add_score(username, role, avatar, student_username):
    if role != "teacher":
        return "Access denied", 403

    score = int(request.form.get("score"))
    users[student_username]["progress"].append(score)

    if score > users[student_username]["high_score"]:
        users[student_username]["high_score"] = score

    return redirect(url_for("view_student",
                            username=username,
                            role=role,
                            avatar=avatar,
                            student_username=student_username))

# -----------------------------------
# Add House Points
# -----------------------------------

@app.route("/add-house-points/<username>/<role>/<avatar>/<student_username>", methods=["POST"])
def add_house_points(username, role, avatar, student_username):
    if role != "teacher":
        return "Access denied", 403

    points = int(request.form.get("points"))
    users[student_username]["house_points"] += points

    return redirect(url_for("view_student",
                            username=username,
                            role=role,
                            avatar=avatar,
                            student_username=student_username))

# -----------------------------------
# Add Behaviour Points
# -----------------------------------

@app.route("/add-behaviour/<username>/<role>/<avatar>/<student_username>", methods=["POST"])
def add_behaviour(username, role, avatar, student_username):
    if role != "teacher":
        return "Access denied", 403

    points = int(request.form.get("points"))
    reason = request.form.get("reason")

    entry = {
        "date": today_str(),
        "points": points,
        "reason": reason
    }

    users[student_username]["behaviour_points"].append(entry)

    return redirect(url_for("view_student",
                            username=username,
                            role=role,
                            avatar=avatar,
                            student_username=student_username))

# -----------------------------------
# House Leaderboard
# -----------------------------------

@app.route("/house-leaderboard/<username>/<role>/<avatar>")
def house_leaderboard(username, role, avatar):
    if role != "teacher":
        return "Access denied", 403

    totals = {"red": 0, "blue": 0, "green": 0, "yellow": 0}

    for data in users.values():
        if data["role"] == "student":
            totals[data["house"]] += data["house_points"]

    return render_template("house_leaderboard.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           totals=totals)

# -----------------------------------
# Daily Register
# -----------------------------------

@app.route("/register/<username>/<role>/<avatar>", methods=["GET", "POST"])
def register(username, role, avatar):
    if role != "teacher":
        return "Access denied", 403

    today = today_str()

    if request.method == "POST":
        for uname, data in users.items():
            if data["role"] == "student":
                status = request.form.get(uname)
                data["attendance"].append({"date": today, "status": status})

        return redirect(url_for("dashboard",
                                username=username,
                                role=role,
                                avatar=avatar))

    student_list = [u for u in users if users[u]["role"] == "student"]

    return render_template("register.html",
                           username=username,
                           role=role,
                           avatar=avatar,
                           students=student_list,
                           users=users,
                           today=today)
    
@app.route("/announcements/<username>/<role>/<avatar>")
def announcements(username, role, avatar):
    data = load_json("announcements.json")
    announcements_list = data.get("announcements", [])
    return render_template(
        "announcements.html",
        username=username,
        role=role,
        avatar=avatar,
        announcements=announcements_list
    )


@app.route("/add-announcement/<username>/<role>/<avatar>", methods=["GET", "POST"])
def add_announcement(username, role, avatar):
    if role != "teacher":
        return "Access denied. Only teachers can add announcements.", 403

    data = load_json("announcements.json")
    announcements_list = data.get("announcements", [])

    message = None

    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")

        if not title or not body:
            message = "Please fill in both title and message."
        else:
            new_announcement = {
                "title": title,
                "message": body,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "author": username
            }
            announcements_list.append(new_announcement)
            data["announcements"] = announcements_list
            save_json("announcements.json", data)
            return redirect(url_for("announcements",
                                    username=username,
                                    role=role,
                                    avatar=avatar))

    return render_template(
        "add_announcement.html",
        username=username,
        role=role,
        avatar=avatar,
        message=message
    )
@app.route("/grades/<username>/<role>/<avatar>")
    def grades(username, role, avatar):
        data = load_json("grades.json")
        all_grades = data.get("grades", {})
        user_grades = all_grades.get(username, [])
        return render_template("grades.html", username=username, role=role, avatar=avatar, grades=user_grades)
    
@app.route("/add-grade/<username>/<role>/<avatar>", methods=["GET", "POST"])
    def add_grade(username, role, avatar):
        if role != "teacher":
            return "Access denied. Only teachers can add grades.", 403

    data = load_json("grades.json")
    all_grades = data.get("grades", {})

    message = None

    if request.method == "POST":
        student = request.form.get("student")
        subject = request.form.get("subject")
        grade = request.form.get("grade")

        if not student or not subject or not grade:
            message = "Please fill in all fields."
        else:
            entry = {
                "subject": subject,
                "grade": grade,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            if student in all_grades:
                all_grades[student].append(entry)
            else:
                all_grades[student] = [entry]
            data["grades"] = all_grades
            save_json("grades.json", data)
            return redirect(url_for("grades", username=username, role=role, avatar=avatar))

    return render_template("add_grade.html", username=username, role=role, avatar=avatar, message=message)
@app.route("/calendar/<username>/<role>/<avatar>")
def calendar_page(username, role, avatar):
    data = load_json("calendar.json")
    events = data.get("events", [])
    return render_template(
        "calendar.html",
        username=username,
        role=role,
        avatar=avatar,
        events=events
    )


@app.route("/add-event/<username>/<role>/<avatar>", methods=["GET", "POST"])
def add_event(username, role, avatar):
    if role != "teacher":
        return "Access denied. Only teachers can add events.", 403

    data = load_json("calendar.json")
    events = data.get("events", [])

    message = None

    if request.method == "POST":
        title = request.form.get("title")
        date = request.form.get("date")
        description = request.form.get("description")

        if not title or not date or not description:
            message = "Please fill in all fields."
        else:
            new_event = {
                "title": title,
                "date": date,
                "description": description,
                "created_by": username
            }
            events.append(new_event)
            data["events"] = events
            save_json("calendar.json", data)
            return redirect(url_for("calendar_page",
                                    username=username,
                                    role=role,
                                    avatar=avatar))

    return render_template(
        "add_event.html",
        username=username,
        role=role,
        avatar=avatar,
        message=message
    )
# -----------------------------------
# Run App
# -----------------------------------

if __name__ == "__main__":
    app.run(debug=True)




