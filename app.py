import os
from pathlib import Path
from flask import Flask, send_from_directory, request, abort
import smtplib
from email.message import EmailMessage

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

# ---- Serve index.html at root ----
@app.route("/")
def home():
    index_path = BASE_DIR / "index.html"
    if index_path.exists():
        return send_from_directory(str(BASE_DIR), "index.html")
    abort(404)

# ---- Serve CSS, JS, Fonts, Images ----
@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory(BASE_DIR / "css", filename)

@app.route("/js/<path:filename>")
def js(filename):
    return send_from_directory(BASE_DIR / "js", filename)

@app.route("/fonts/<path:filename>")
def fonts(filename):
    return send_from_directory(BASE_DIR / "fonts", filename)

@app.route("/images/<path:filename>")
def images(filename):
    return send_from_directory(BASE_DIR / "images", filename)

# ---- Handle form submission ----
@app.route("/send_mail", methods=["POST"])
def send_mail():
    name = request.form.get("name", "(no name)")
    email = request.form.get("email", "(no email)")
    message = request.form.get("comment", "(no message)")

    # mail_user = "WEBSITE.EMAIL.STUEBER@gmail.com"
    # mail_pass = "qbaf poje vwbh tghh"
    # mail_to   = "kstueber@holycross.edu" or mail_user

    if not (mail_user and mail_pass and mail_to):
        return "Server email is not configured. Set MAIL_USER, MAIL_PASS, MAIL_TO.", 500

    msg = EmailMessage()
    msg["Subject"] = "New Contact Form Submission"
    msg["From"] = mail_user
    msg["To"] = mail_to
    msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(mail_user, mail_pass)
        s.send_message(msg)

    return "Message sent!"

