from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session handling

@app.route("/results", methods=["GET", "POST"])
def results():
    if "admin" not in session:
        return redirect(url_for("admin_login"))  # Redirect if not logged in
    return render_template("results.html", votes=load_votes())

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]
        if password == "your_secure_password":  # Change this to a strong password
            session["admin"] = True
            return redirect(url_for("results"))
    return render_template("admin-login.html")
