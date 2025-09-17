from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

CSV_FILE = "data.csv"

# Ensure CSV exists with required columns
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=[
        "Username", "Password", "Role", "Name", "RegNo", "Email",
        "Room", "Block", "Complaints", "Status"
    ])
    df.to_csv(CSV_FILE, index=False)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        df = pd.read_csv(CSV_FILE)

        user = df[(df["Username"] == username) & 
                  (df["Password"] == password) & 
                  (df["Role"] == role)]

        if not user.empty:
            if role == "student":
                return redirect(url_for("complaints", username=username))
            elif role == "warden":
                return redirect(url_for("warden"))
        else:
            flash("❌ Invalid credentials. Try again.", "danger")
            return redirect(url_for("login")) 
    
    return render_template("login.html")

@app.route("/complaints/<username>", methods=["GET", "POST"])
def complaints(username):
    if request.method == "POST":
        regno = request.form["regno"]
        email = request.form["email"]
        room = request.form["room"]
        block = request.form["block"]
        category = request.form["category"]
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]

        df = pd.read_csv(CSV_FILE)

        if username in df["Username"].values:
            df.loc[df["Username"] == username, ["RegNo","Email","Room","Block"]] = [regno,email,room,block]
            complaint_text = f"[{category}] {title} - {description} (Priority: {priority})"
            df.loc[df["Username"] == username, "Complaints"] = complaint_text
            df.loc[df["Username"] == username, "Status"] = "Not Resolved"   # default
            df.to_csv(CSV_FILE, index=False)

            flash("✅ Complaint submitted successfully!", "success")
            return redirect(url_for("complaints", username=username))

    return render_template("complaints.html", username=username)

@app.route("/warden")
def warden():
    df = pd.read_csv(CSV_FILE)

    # Only show users who submitted complaints
    complaints = df[df["Complaints"].notna()]

    if complaints.empty:
        flash("📭 No complaints submitted yet.", "info")
        return render_template("warden.html", complaints=[])

    return render_template("warden.html", complaints=complaints.to_dict(orient="records"))

@app.route("/update_status", methods=["POST"])
def update_status():
    regno = request.form["regno"]
    new_status = request.form["status"]

    df = pd.read_csv(CSV_FILE)

    if regno in df["RegNo"].values:
        df.loc[df["RegNo"] == regno, "Status"] = new_status
        df.to_csv(CSV_FILE, index=False)
        flash(f"✅ Status updated for RegNo: {regno}", "success")
    else:
        flash("❌ Complaint not found!", "danger")

    return redirect(url_for("warden"))

if __name__ == "__main__":
    app.run(debug=True)
