from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "zeyra_secret_key"

# ======================
# رفع الملفات
# ======================
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ======================
# الصفحات الأساسية
# ======================

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/services")
def services():
    return render_template("services.html")

# ======================
# CONTACT
# ======================

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO messages (name, subject, message)
        VALUES (?, ?, ?)
        """, (
            request.form.get("name"),
            request.form.get("subject"),
            request.form.get("message")
        ))

        conn.commit()
        conn.close()

        return redirect("/contact")

    return render_template("contact.html")

# ======================
# CAREERS
# ======================

@app.route("/careers", methods=["GET", "POST"])
def careers():
    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        age = request.form.get("age")
        national_id = request.form.get("national_id")
        english_level = request.form.get("english_level")

        cv = request.files.get("cv")
        id_front = request.files.get("id_front")
        id_back = request.files.get("id_back")

        cv_name = cv.filename if cv else ""
        front_name = id_front.filename if id_front else ""
        back_name = id_back.filename if id_back else ""

        if cv:
            cv.save(os.path.join(app.config["UPLOAD_FOLDER"], cv_name))
        if id_front:
            id_front.save(os.path.join(app.config["UPLOAD_FOLDER"], front_name))
        if id_back:
            id_back.save(os.path.join(app.config["UPLOAD_FOLDER"], back_name))

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO applicants 
        (name, email, phone, age, national_id, english_level, cv, id_front, id_back)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, email, phone, age,
            national_id, english_level,
            cv_name, front_name, back_name
        ))

        conn.commit()
        conn.close()

        return redirect("/careers")

    return render_template("careers.html")

# ======================
# LOGIN
# ======================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "Ammar" and password == "Ammar123456":
            session["admin"] = True   # ✅ توحيد الاسم
            return redirect("/admin")
        else:
            return render_template("login.html", error="Wrong login")

    return render_template("login.html")

# ======================
# ADMIN PAGE
# ======================

@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM applicants")
    applicants = c.fetchall()

    conn.close()

    return render_template("admin.html", applicants=applicants)

# ======================
# DELETE APPLICANT
# ======================

@app.route("/delete/<int:id>")
def delete(id):
    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("DELETE FROM applicants WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")

# ======================
# LOGOUT
# ======================

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")

# ======================
# RUN
# ======================

if __name__ == "__main__":
    app.run(debug=True)