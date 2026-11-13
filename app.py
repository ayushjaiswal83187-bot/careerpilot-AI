from flask import Flask, render_template, request, redirect, session, url_for
from db import Base, engine, SessionLocal
import models
import ai_logic
import PyPDF2
import docx
import json

app = app = Flask(_name_, template_folder='.', static_folder='.')
app.secret_key = "career_pilot_secret"
Base.metadata.create_all(bind=engine)

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    db = SessionLocal()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        existing_user = db.query(models.User).filter_by(email=email).first()
        if existing_user:
            db.close()
            return "User already exists! <a href='/login'>Login</a>"
        user = models.User(email=email, password=password)
        db.add(user)
        db.commit()
        db.close()
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    db = SessionLocal()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.query(models.User).filter_by(email=email, password=password).first()
        if user:
            session["user"] = user.email
            db.close()
            return redirect(url_for("dashboard"))
        db.close()
        return "Invalid credentials! <a href='/login'>Try again</a>"
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    results = None
    db = SessionLocal()
    if request.method == "POST":
        user_goal = request.form.get("role")
        resume_text = request.form.get("resume")
        file = request.files.get("file")
        if file and file.filename != "":
            if file.filename.endswith(".pdf"):
                pdf_reader = PyPDF2.PdfReader(file)
                resume_text = "".join([p.extract_text() for p in pdf_reader.pages])
            elif file.filename.endswith(".docx"):
                doc = docx.Document(file)
                resume_text = "\n".join([p.text for p in doc.paragraphs])
        if resume_text and user_goal:
            results = ai_logic.analyze_resume(resume_text, user_goal)
            user = db.query(models.User).filter_by(email=session["user"]).first()
            report = models.Report(user_id=user.id, resume_text=resume_text, results=json.dumps(results))
            db.add(report)
            db.commit()
    db.close()
    return render_template("dashboard.html", user=session["user"], result=results)

# --- NAYA CHAT FEATURE ROUTE ---
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect(url_for("login"))
    bot_response = None
    if request.method == "POST":
        user_query = request.form.get("query")
        bot_response = ai_logic.get_ai_answer(user_query) 
    return render_template("chat.html", response=bot_response)

@app.route("/history")
def history():
    if "user" not in session:
        return redirect(url_for("login"))
    db = SessionLocal()
    user = db.query(models.User).filter_by(email=session["user"]).first()
    reports = db.query(models.Report).filter_by(user_id=user.id).all()
    parsed_reports = [{"resume": r.resume_text, "result": json.loads(r.results)} for r in reports]
    db.close()
    return render_template("history.html", reports=parsed_reports)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
