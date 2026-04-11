from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# tell flask ke html files current folder me hain
app = Flask(__name__, template_folder='.')

# ===============================
# DATABASE FUNCTION
# ===============================
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ===============================
# DATABASE CREATE (auto)
# ===============================
def create_table():
    conn = get_db_connection()

    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    conn.close()

create_table()

# ===============================
# HOME PAGE
# ===============================
@app.route("/")
def home():
    return render_template("home.html")

# ===============================
# SIGNUP
# ===============================
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")

# ===============================
# LOGIN
# ===============================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        conn.close()

        if user:
            return redirect(url_for("result", username=user["username"],email=user["email"]))
        else:
            return "Invalid email or password"

    return render_template("login.html")

# ===============================
# RESULT PAGE
# ===============================
@app.route("/result")
def result():
    username = request.args.get("username")
    email = request.args.get("email")
    return render_template("result.html", username=username, email=email)

# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    app.run(debug=True)