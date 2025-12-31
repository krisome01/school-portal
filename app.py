import json
import os

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = {
    "student1": "password123",
    "teacher": "teach2025"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            return redirect(url_for("dashboard", username=username))
        else:
            return "<h1>Login failed</h1><p><a href='/login'>Try again</a></p>"

    return render_template("login.html")

@app.route("/dashboard/<username>")
def dashboard(username):
    return render_template("dashboard.html", username=username, title="Dashboard")

announcements_list = [
    {"date": "January 6", "emoji": "📅", "text": "School reopens"},
    {"date": "February 12", "emoji": "📝", "text": "Mock exams start"},
    {"date": "March 3", "emoji": "👨‍👩‍👧", "text": "Year 7 Parents Evening"}
]

@app.route("/announcements", methods=["GET", "POST"])
def announcements():
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
        username="student1"  # You can make this dynamic later
    )

@app.route("/grades")
def grades():
    return render_template("grades.html", title="Grades")

@app.route("/profile/<username>")
def profile(username):
    return render_template("profile.html", username=username, title="Profile")

@app.route("/logout")
def logout():
    return redirect(url_for("home"))

# REMOVE app.run() — Render will run the app using gunicorn



