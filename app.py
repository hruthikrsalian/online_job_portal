from flask import Flask, render_template, request, redirect, session
import sqlite3, random, hashlib, time, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pdfminer.high_level import extract_text


app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "easyjob"

ADMIN_EMAIL = "admin@easyjob.com"
ADMIN_PASSWORD = "admin123"
import smtplib
SKILL_LIST = [
  "python","java","c","c++","sql","mysql","mongodb",
  "html","css","javascript","react","node","flask",
  "django","spring","rest","api","git","docker",
  "kubernetes","aws","linux","ml","data","r"
]

GLOBAL_SKILLS = [
  "python","java","c","c++","javascript","react","angular",
  "flask","django","fastapi","spring",
  "sql","mysql","postgres","mongodb",
  "aws","azure","gcp","docker","kubernetes",
  "git","github","linux","html","css"
]
import re
def valid_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email)

def strong_password(pw):
    return re.match(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$",
        pw
    )

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def create_offer_letter(name, company, role, stipend, ctc):
    filename = f"static/offers/{name}_offer.pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>OFFER LETTER</b>", styles["Title"]))
    story.append(Spacer(1, 20))

    content = f"""
    Dear {name},<br/><br/>

    Congratulations! We are pleased to offer you the position of 
    <b>{role}</b> at <b>{company}</b>.<br/><br/>

    Monthly Stipend: <b>{stipend}</b><br/>
    Annual CTC: <b>{ctc}</b><br/><br/>

    We look forward to your valuable contribution.<br/><br/>

    Regards,<br/>
    HR Department<br/>
    {company}
    """

    story.append(Paragraph(content, styles["BodyText"]))
    doc.build(story)

    return filename


def extract_skills_section(resume_text):
    text = resume_text.lower()

    # find SKILLS section only
    match = re.search(
        r"skills(.*?)(education|projects|experience|certifications|$)",
        text,
        re.S
    )

    if not match:
        return []

    skills_block = match.group(1)

    raw_skills = re.split(r"[,\n•|-]", skills_block)

    skills = []
    for s in raw_skills:
        s = s.strip()
        if len(s) > 1:
            skills.append(s)

    return skills


def send_mail(uid, msg, attachment=None):
    from_email = "easyyyyjob123@gmail.com"
    password = "wogb anza ilsg rqbj"

    con = db()
    to_email, name = con.execute(
        "SELECT email,name FROM users WHERE id=?",(uid,)
    ).fetchone()
    con.close()

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = "Offer Letter - Congratulations!"

    message.attach(MIMEText(msg, "plain"))

    # attach pdf
    if attachment:
        with open(attachment, "rb") as f:
            part = MIMEText(f.read(), "base64", "utf-8")
            part["Content-Disposition"] = f'attachment; filename="offer_letter.pdf"'
            message.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        print("MAIL + PDF SENT")
    except Exception as e:
        print("MAIL FAILED:", e)



@app.route("/final_select/<int:appid>/<int:jid>")
def final_select(appid, jid):

    con = db()

    # update status
    con.execute("""
        UPDATE applications
        SET status='SELECTED'
        WHERE id=? AND job_id=?
    """, (appid, jid))

    # fetch correct data
    row = con.execute("""
        SELECT 
            u.id,           -- candidate id
            u.name,         -- candidate name
            j.company,      -- company name
            j.title         -- job title
        FROM applications a
        JOIN users u ON u.id = a.user_id
        JOIN jobs j ON j.id = a.job_id
        WHERE a.id=?
    """, (appid,)).fetchone()

    con.commit()
    con.close()

    uid, candidate_name, company, role = row

    # dummy values
    stipend = "₹25,000/month"
    ctc = "₹4.5 LPA"

    # create offer letter PDF
    pdf_path = create_offer_letter(
        candidate_name,
        company,
        role,
        stipend,
        ctc
    )

    msg = f"""
Congratulations {candidate_name}!

You are selected for the position of {role}
at {company}.

Offer letter attached.
"""

    send_mail(uid, msg, pdf_path)

    return redirect(request.referrer)



@app.route("/final_reject/<int:appid>/<int:jid>")
def final_reject(appid, jid):
    con = db()
    con.execute("""
      UPDATE applications 
      SET status='FINAL_REJECTED' 
      WHERE id=? AND job_id=?
    """,(appid,jid))
    con.commit()
    con.close()

    con = db()
    uid = con.execute(
        "SELECT user_id FROM applications WHERE id=?",(appid,)
    ).fetchone()[0]
    con.close()

    send_mail(uid, "Sorry, you were not selected.")
    return redirect(request.referrer)


# ALWAYS use same DB file (no matter where you run from)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "easyjob.db")

def db():
    return sqlite3.connect(DB_PATH)

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()
def pdf_to_text(path):
    return extract_text(path).lower()

def skill_match(resume_text, job_skills):
    resume_text = resume_text.lower()
    job_keywords = [k.strip().lower() for k in job_skills.split(",")]

    matched = []

    for skill in SKILL_LIST:
        if skill in resume_text:
            if skill in job_keywords:
                matched.append(skill)

    percent = (len(matched) / len(job_keywords)) * 100
    return round(percent, 2), matched




# ---------- DB INIT ----------
def init():
    con = db()
    c = con.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT,
        role TEXT,
        approved INTEGER
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY,
        title TEXT,
        company TEXT,
        descr TEXT,
        skills TEXT,
        hr_id INTEGER
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY,
        section TEXT,
        q TEXT,
        a TEXT,
        b TEXT,
        c TEXT,
        d TEXT,
        ans TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS results(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        job_id INTEGER,
        score INTEGER
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS applications(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        job_id INTEGER,
        skills TEXT,
        resume TEXT,
        status TEXT,
        match_score REAL,
        parsed_skills TEXT
    )""")

    con.commit()
    con.close()
    

init()
from flask import jsonify

@app.route("/api/questions")
def api_questions():
    if "u" not in session or session["u"][4] != "candidate":
        return jsonify([])

    qs = []
    con = db()
    for s in ["logical","gk","english","math","c"]:
        allq = con.execute(
            "SELECT * FROM questions WHERE section=?", (s,)
        ).fetchall()

        if len(allq) < 5:
            return jsonify([])

        qs += random.sample(allq,5)

    con.close()
    return jsonify(qs)


# ---------- HOME ----------
@app.route("/", methods=["GET","POST"])
def home():
    mode = request.args.get("mode")
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        # ---------- LOGIN ----------
        if action == "login":
            email = request.form["email"].strip().lower()
            password = request.form["password"]

            # Fixed admin
            if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                session["u"] = ("admin", "Admin", ADMIN_EMAIL, "", "admin", 1)
                return redirect("/admin")

            con = db()
            u = con.execute(
                "SELECT * FROM users WHERE email=? AND password=?",
                (email, hash_pw(password))
            ).fetchone()
            con.close()

            if not u:
                error = "Account not found. Please register."
                mode = "login"
            else:
                session["u"] = u
                if u[4] == "hr":
                    return redirect("/hr")
                return redirect("/candidate")

        # ---------- REGISTER ----------
        elif action == "register":
            name = request.form["name"]
            email = request.form["email"].strip().lower()
            password = request.form["password"]
            role = request.form["role"]

            if not valid_email(email):
                return render_template(
                    "home.html",
                    mode="register",
                    error="Use valid Gmail address"
                )

            if not strong_password(password):
                return render_template(
                    "home.html",
                    mode="register",
                    error="Password too weak"
                )

            con = db()
            con.execute("INSERT INTO users VALUES(NULL,?,?,?,?,0)", (
                name,
                email,
                hash_pw(password),
                role
            ))
            con.commit()
            con.close()

            return redirect("/?mode=login")

    return render_template("home.html", mode=mode, error=error)

# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    if "u" not in session or session["u"][4] != "admin":
        return redirect("/")

    con = db()

    hrs = con.execute("""
      SELECT id, name, email, approved 
      FROM users 
      WHERE role='hr'
    """).fetchall()

    candidates = con.execute("""
      SELECT id, name, email 
      FROM users 
      WHERE role='candidate'
    """).fetchall()

    con.close()
    return render_template("admin.html", hrs=hrs, candidates=candidates)


@app.route("/approve/<int:i>")
def approve(i):
    if session["u"][4] != "admin":
        return redirect("/")
    con = db()
    con.execute("UPDATE users SET approved=1 WHERE id=?", (i,))
    con.commit()
    con.close()
    return redirect("/admin")

# ---------- HR ----------
@app.route("/hr", methods=["GET","POST"])
def hr():
    if session["u"][4] != "hr":
        return redirect("/")
    if session["u"][5] == 0:
        return "Waiting for admin approval"

    if request.method == "POST":
        con = db()
        con.execute("INSERT INTO jobs VALUES(NULL,?,?,?,?,?)",
(
 request.form["title"],      # title
 request.form["company"],    # company
 request.form["desc"],
 request.form["skills"],
 session["u"][0]
))



        con.commit()
        con.close()

    con = db()
    jobs = con.execute(
    "SELECT * FROM jobs WHERE hr_id=?",
    (session["u"][0],)
).fetchall()

    con.close()
    return render_template("hr.html", jobs=jobs)

# ---------- CANDIDATE ----------
@app.route("/candidate")
def candidate():
    if session["u"][4] != "candidate":
        return redirect("/")
    con = db()
    jobs = con.execute("""
 SELECT * FROM jobs WHERE id NOT IN (
   SELECT job_id FROM applications WHERE user_id=?
 )
""",(session["u"][0],)).fetchall()

    apps = con.execute("""
 SELECT j.company, j.title, a.status, j.id
 FROM applications a
 JOIN jobs j ON j.id=a.job_id
 WHERE a.user_id=?
""",(session["u"][0],)).fetchall()


    con.close()
    return render_template("candidate.html", jobs=jobs, apps=apps)


# ---------- TEST ----------
@app.route("/test/<int:jid>")
def test(jid):
    if session["u"][4] != "candidate":
        return redirect("/")

    con = db()

    # 🔒 BLOCK unless HR approved
    check = con.execute(
        "SELECT status FROM applications WHERE user_id=? AND job_id=?",
        (session["u"][0], jid)
    ).fetchone()

    if not check or check[0] != "APPROVED":
        con.close()
        return "You are not approved by HR yet."

    # 🔒 BLOCK if already attempted
    attempted = con.execute(
        "SELECT * FROM results WHERE user_id=? AND job_id=?",
        (session["u"][0], jid)
    ).fetchone()

    if attempted:
        con.close()
        return "You have already attempted this test."

    # normal test logic
    qs = []
    for s in ["logical","gk","english","math","c"]:
        allq = con.execute(
            "SELECT * FROM questions WHERE section=?", (s,)
        ).fetchall()
        qs += random.sample(allq,5)

    con.close()

    session["qs"] = qs
    session["jid"] = jid
    session["start"] = time.time()

    return render_template("test.html", qs=qs)



# ---------- SUBMIT ----------
@app.route("/submit", methods=["POST"])
def submit():
    score = 0
    for q in session["qs"]:
        if request.form.get(str(q[0])) == q[7]:
            score += 1

    con = db()
    con.execute("INSERT INTO results VALUES(NULL,?,?,?)",
        (session["u"][0], session["jid"], score))
    con.commit()
    con.close()

    return render_template("test_success.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- DEBUG (optional but useful) ----------
@app.route("/debug")
def debug():
    con = db()
    data = con.execute("SELECT * FROM users").fetchall()
    con.close()
    return str(data)

@app.route("/job/<int:jid>", methods=["GET","POST"])
def job_details(jid):
    if session["u"][4] != "candidate":
        return redirect("/")

    con = db()

    # RULE 1: Block duplicate applications
    exists = con.execute(
        "SELECT * FROM applications WHERE user_id=? AND job_id=?",
        (session["u"][0], jid)
    ).fetchone()

    if exists:
        con.close()
        return "You have already applied for this job."

    if request.method == "POST":
        file = request.files["resume"]
        filename = file.filename
        path = "static/resumes/" + filename
        file.save(path)

        resume_text = pdf_to_text(path)

        found = []
        for s in GLOBAL_SKILLS:
            if s in resume_text:
                found.append(s)

        job = con.execute(
            "SELECT * FROM jobs WHERE id=?", (jid,)
        ).fetchone()

        score, matched_skills = skill_match(resume_text, job[4])
        parsed = ",".join(matched_skills)

        con.execute("""
            INSERT INTO applications 
            (user_id, job_id, skills, resume, status, match_score, parsed_skills)
            VALUES(?,?,?,?,?,?,?)
        """, (
            session["u"][0],
            jid,
            request.form["skills"],
            filename,
            "PENDING",
            score,
            parsed
        ))

        con.commit()
        con.close()

        return redirect("/candidate")

    job = con.execute(
        "SELECT * FROM jobs WHERE id=?", (jid,)
    ).fetchone()

    con.close()

    return render_template("job_details.html", job=job)

@app.route("/applications/<int:jid>")
def view_applications(jid):
    con = db()
    apps = con.execute("""
      SELECT a.id,
             u.name || ' (' || u.email || ')',
             a.skills,
             a.resume,
             a.status,
             a.match_score,
             a.parsed_skills,
             IFNULL(r.score, 'Not Attempted')
      FROM applications a
      JOIN users u ON u.id = a.user_id
      LEFT JOIN results r 
           ON r.user_id = a.user_id 
          AND r.job_id = a.job_id
      WHERE a.job_id = ?
    """,(jid,)).fetchall()
    con.close()
    return render_template("applications.html", apps=apps, jid=jid)



@app.route("/approve_app/<int:i>")
def approve_app(i):
    con = db()
    con.execute(
      "UPDATE applications SET status='APPROVED' WHERE id=?",(i,))
    con.commit()
    con.close()
    return redirect(request.referrer)

@app.route("/reject_app/<int:i>")
def reject_app(i):
    con = db()
    con.execute(
      "UPDATE applications SET status='RESUME_REJECTED' WHERE id=?",(i,))
    con.commit()
    con.close()
    return redirect(request.referrer)

@app.route("/match/<int:appid>")
def view_match(appid):
    con = db()
    data = con.execute("""
      SELECT j.skills, a.resume
      FROM applications a
      JOIN jobs j ON j.id = a.job_id
      WHERE a.id=?
    """,(appid,)).fetchone()
    con.close()

    job_skills = [s.strip().lower() for s in data[0].split(",")]
    resume_path = "static/resumes/" + data[1]

    resume_text = pdf_to_text(resume_path)

    skill_data = []
    matched = 0

    for s in job_skills:
        found = 1 if s in resume_text else 0
        if found:
            matched += 1
        skill_data.append({
            "skill": s,
            "value": 100 if found else 0
        })

    return render_template(
        "match_view.html",
        skill_data=skill_data,
        matched=matched,
        total=len(job_skills)
    )

@app.route("/delete_job/<int:jid>")
def delete_job(jid):
    con = db()
    con.execute(
        "DELETE FROM jobs WHERE id=? AND hr_id=?",
        (jid, session["u"][0])
    )
    con.commit()
    con.close()
    return redirect("/hr")

@app.route("/edit_job/<int:jid>", methods=["GET","POST"])
def edit_job(jid):
    con = db()

    if request.method == "POST":
        con.execute("""
          UPDATE jobs 
          SET title=?, company=?, descr=?, skills=? 
          WHERE id=? AND hr_id=?
        """, (
            request.form["title"],
            request.form["company"],
            request.form["desc"],
            request.form["skills"],
            jid,
            session["u"][0]
        ))
        con.commit()
        con.close()
        return redirect("/hr")

    job = con.execute(
        "SELECT * FROM jobs WHERE id=? AND hr_id=?",
        (jid, session["u"][0])
    ).fetchone()
    con.close()

    return render_template("edit_job.html", job=job)

@app.route("/hr_entry")
def hr_entry():
    if "u" not in session:
        return redirect("/?mode=login")

    if session["u"][4] != "hr":
        return "Only HR can post jobs."

    return redirect("/hr")


@app.route("/candidate_entry")
def candidate_entry():
    if "u" not in session:
        return redirect("/?mode=login")

    if session["u"][4] != "candidate":
        return "Only candidates can search jobs."

    return redirect("/candidate")

@app.route("/admin_approve/<int:uid>")
def admin_approve(uid):
    con = db()
    con.execute("UPDATE users SET approved=1 WHERE id=?", (uid,))
    con.commit()
    con.close()
    return redirect("/admin")


@app.route("/admin_reject/<int:uid>")
def admin_reject(uid):
    con = db()
    con.execute("UPDATE users SET approved=-1 WHERE id=?", (uid,))
    con.commit()
    con.close()
    return redirect("/admin")


@app.route("/admin_delete/<int:uid>")
def admin_delete(uid):
    con = db()
    con.execute("DELETE FROM users WHERE id=?", (uid,))
    con.commit()
    con.close()
    return redirect("/admin")

import re

def extract_resume_summary(resume_text):
    summary = {}

    # Email
    email = re.search(r"[\w\.-]+@[\w\.-]+", resume_text)
    summary["email"] = email.group(0) if email else "Not found"

    # Phone
    phone = re.search(r"\+?\d{10,13}", resume_text)
    summary["phone"] = phone.group(0) if phone else "Not found"

    # Skills
    skills = extract_skills_section(resume_text)
    summary["skills"] = skills

    # Education
    edu_match = re.search(r"(education.*?)(skills|projects|experience|$)", resume_text, re.S)
    summary["education"] = edu_match.group(1).strip()[:400] if edu_match else "Not found"

    # Projects
    proj_match = re.search(r"(projects.*?)(skills|education|experience|$)", resume_text, re.S)
    summary["projects"] = proj_match.group(1).strip()[:400] if proj_match else "Not found"

    return summary

@app.route("/resume_details/<int:app_id>")
def resume_details(app_id):
    con = db()
    app = con.execute(
        "SELECT resume FROM applications WHERE id=?",
        (app_id,)
    ).fetchone()
    con.close()

    path = "static/resumes/" + app[0]
    text = pdf_to_text(path)

    summary = extract_resume_summary(text)

    return render_template("resume_details.html", summary=summary)


if __name__ == "__main__":
    app.run(debug=True)