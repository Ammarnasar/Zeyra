from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "zeyra_secret_key"

# ======================
# إعداد رفع الملفات
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

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        subject = request.form.get("subject")
        message = request.form.get("message")

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO messages (name, subject, message)
        VALUES (?, ?, ?)
        """, (name, subject, message))

        conn.commit()
        conn.close()

        return redirect(url_for("contact"))

    return render_template("contact.html")

# ======================
# التوظيف
# ======================

@app.route("/careers", methods=["GET", "POST"])
def careers():
    if request.method == "POST":
        try:
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

        except Exception as e:
            print("Error:", e)

        return redirect(url_for("careers"))

    return render_template("careers.html")

# ======================
# تسجيل دخول الأدمن
# ======================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "Ammar" and password == "Ammar123456":
            session["ammar"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Wrong username or password")

    return render_template("login.html")

# ======================
# Dashboard (محمية)
# ======================

@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM applicants")
    applicants = c.fetchall()

    c.execute("SELECT * FROM messages")
    messages = c.fetchall()

    conn.close()

    return render_template("dashboard.html", applicants=applicants, messages=messages)

# ======================
# حذف متقدم
# ======================

@app.route("/delete_applicant/<int:id>")
def delete_applicant(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("DELETE FROM applicants WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

# ======================
# حذف رسالة
# ======================

@app.route("/delete_message/<int:id>")
def delete_message(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("DELETE FROM messages WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

# ======================
# تسجيل الخروج
# ======================

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

# ======================
# تشغيل التطبيق
# ======================

if __name__ == "__main__":
    app.run(debug=True)