from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "zeyra_secret_key"

# ======================
# Upload Folder
# ======================
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ======================
# DB
# ======================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ======================
# Home
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
        conn = get_db()
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
# CAREERS 🔥
# ======================
@app.route("/careers", methods=["GET", "POST"])
def careers():
    if request.method == "POST":

        # ======================
        # 🔥 البيانات
        # ======================
        first_name = request.form.get("first_name")
        middle_name = request.form.get("middle_name")
        last_name = request.form.get("last_name")

        name = f"{first_name} {middle_name or ''} {last_name}"

        email = request.form.get("email")
        phone = request.form.get("phone")
        phone_alt = request.form.get("phone_alt")

        dob = request.form.get("date_of_birth")
        nationality = request.form.get("nationality")
        national_id = request.form.get("national_id")
        address = request.form.get("address")

        gender = request.form.get("gender")
        marital_status = request.form.get("marital_status")

        # ======================
        # 🎓 Education
        # ======================
        degree = request.form.get("degree")
        major = request.form.get("major")
        graduation_year = request.form.get("graduation_year")

        # ======================
        # 💼 Experience
        # ======================
        experience_years = request.form.get("experience_years")
        employment_status = request.form.get("employment_status")
        current_salary = request.form.get("current_salary")
        expected_salary = request.form.get("expected_salary")

        # ======================
        # 🧠 Skills
        # ======================
        skills = request.form.get("skills")

        # ======================
        # 🌍 Language
        # ======================
        language = request.form.get("language")
        language_level = request.form.get("language_level")

        # ======================
        # 📂 Files
        # ======================
        cv = request.files.get("cv")
        id_front = request.files.get("id_front")
        id_back = request.files.get("id_back")

        cv_name = cv.filename if cv else ""
        front_name = id_front.filename if id_front else ""
        back_name = id_back.filename if id_back else ""

        if cv and cv_name:
            cv.save(os.path.join(app.config["UPLOAD_FOLDER"], cv_name))

        if id_front and front_name:
            id_front.save(os.path.join(app.config["UPLOAD_FOLDER"], front_name))

        if id_back and back_name:
            id_back.save(os.path.join(app.config["UPLOAD_FOLDER"], back_name))

        # ======================
        # 💾 SAVE TO DB
        # ======================
        conn = get_db()
        c = conn.cursor()

        c.execute("""
        INSERT INTO applicants (
            name, email, phone, phone_alt,
            dob, nationality, national_id, address,
            gender, marital_status,
            degree, major, graduation_year,
            experience_years, employment_status,
            current_salary, expected_salary,
            skills,
            language, language_level,
            cv, id_front, id_back
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, email, phone, phone_alt,
            dob, nationality, national_id, address,
            gender, marital_status,
            degree, major, graduation_year,
            experience_years, employment_status,
            current_salary, expected_salary,
            skills,
            language, language_level,
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
        if request.form.get("username") == "Ammar" and request.form.get("password") == "Ammar123456":
            session["admin"] = True
            return redirect("/admin")

        return render_template("login.html", error="Wrong login")

    return render_template("login.html")

# ======================
# ADMIN
# ======================
@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/login")

    conn = get_db()

    applicants = conn.execute("SELECT * FROM applicants ORDER BY id DESC").fetchall()
    messages = conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()

    conn.close()

    return render_template("admin.html", applicants=applicants, messages=messages)

# ======================
# DELETE APPLICANT
# ======================
@app.route("/delete/<int:id>")
def delete(id):
    if "admin" not in session:
        return redirect("/login")

    conn = get_db()
    conn.execute("DELETE FROM applicants WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin")

# ======================
# DELETE MESSAGE
# ======================
@app.route("/delete_message/<int:id>")
def delete_message(id):
    if "admin" not in session:
        return redirect("/login")

    conn = get_db()
    conn.execute("DELETE FROM messages WHERE id = ?", (id,))
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