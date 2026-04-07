from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from flask import session
from flask import session, redirect, url_for

app = Flask(__name__)

app.secret_key = "zeyra_secret_123"
app.secret_key = "zeyra_secret_key"
# إعداد رفع الملفات
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# إنشاء فولدر إذا مش موجود
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
# صفحة التوظيف
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

            # أسماء الملفات
            cv_name = cv.filename if cv else ""
            front_name = id_front.filename if id_front else ""
            back_name = id_back.filename if id_back else ""

            # حفظ الملفات
            if cv:
                cv.save(os.path.join(app.config["UPLOAD_FOLDER"], cv_name))

            if id_front:
                id_front.save(os.path.join(app.config["UPLOAD_FOLDER"], front_name))

            if id_back:
                id_back.save(os.path.join(app.config["UPLOAD_FOLDER"], back_name))

            # تخزين في الداتابيس
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
# Dashboard (الإدارة)
# ======================
@app.route("/dashboard")
def dashboard():
    import sqlite3

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # جلب المتقدمين
    c.execute("SELECT * FROM applicants")
    applicants = c.fetchall()

    # جلب الرسائل
    c.execute("SELECT * FROM messages")
    messages = c.fetchall()

    conn.close()

    return render_template("dashboard.html", applicants=applicants, messages=messages)
# ======================
# الادمن 
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # بيانات الأدمن (تقدر تغيرها)
        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect(url_for("dashboard"))

    return render_template("login.html") 

# ======================
# حذف متقدم  
# ======================
# حذف متقدم
@app.route("/delete_applicant/<int:id>")
def delete_applicant(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("DELETE FROM applicants WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# حذف رسالة
@app.route("/delete_message/<int:id>")
def delete_message(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("DELETE FROM messages WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ======================
# صفحة تسجيل الدخول 
# =======================


        # بيانات الأدمن (تقدر تغيرها)
    if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect("/dashboard")
    else:
            return "Wrong username or password"

    return render_template("login.html")
# ======================
# تسجيل الخروج 
# ======================

# ======================
# تشغيل التطبيق
# ======================

if __name__ == "__main__":
    app.run(debug=True)


    