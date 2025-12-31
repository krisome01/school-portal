import json
import os

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
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            role = users[username]["role"]
            avatar = users[username]["avatar"]
            return redirect(url_for("dashboard", username=username, role=role, avatar=avatar))
        else:
            return "<h1>Login failed</h1><p><a href='/login'>Try again</a></p>"

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

# REMOVE app.run() — Render will run the app using gunicorn










