from flask import Flask, render_template, redirect, request, session, send_file
import os
import shutil

app = Flask(__name__)
app.secret_key = "secret123"

recovered_files = 0


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "HarshCyberSentinel" and password == "Harsh@11":
            session["user"] = username
            return redirect("/dashboard")

        else:
            return "Invalid Credentials"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    global recovered_files

    if "user" not in session:
        return redirect("/")

    logs = []
    attack_count = 0
    attack_data = []

    # ✅ READ LOG FILE PROPERLY
    try:
        with open("logs/logs.txt", "r") as file:
            logs = file.readlines()
            attack_count = len(logs)

            # ✅ CREATE GRAPH DATA (1,2,3,...)
            if attack_count == 0:
              attack_data = [0]
            else:
             attack_data = list(range(1, attack_count + 1))
             attack_labels = [f"Attack {i}" for i in range(1, attack_count + 1)]

    except:
        logs = []
        attack_data = []

    # ✅ STATUS
    status = "stopped"
    try:
        with open("status.txt", "r") as f:
            status = f.read().strip()
    except:
        status = "stopped"

    # ✅ QUARANTINE FILES
    quarantine_files = []
    try:
        quarantine_files = os.listdir("quarantine")
    except:
        quarantine_files = []

    return render_template(
        "index.html",
        logs=logs,
        attack_count=attack_count,
        recovered_files=recovered_files,
        quarantine_files=quarantine_files,
        status=status,
        attack_data=attack_data  ,
    )


# ---------------- RECOVER ----------------
@app.route("/recover")
def recover():

    global recovered_files

    backup = "backup_files"
    target = "test_folder"

    # pause detection
    with open("status.txt", "w") as f:
        f.write("paused")

    try:
        # remove all locked files
        for file in os.listdir(target):
            if file.endswith(".locked"):
                os.remove(os.path.join(target, file))

        # restore original files
        for file in os.listdir(backup):
            src = os.path.join(backup, file)
            dst = os.path.join(target, file)
            shutil.copy(src, dst)

        # get total attacks
        with open("logs/logs.txt", "r") as f:
            total_attacks = len(f.readlines())

        # 🔥 AUTO RECOVERY (SIMULATED PROGRESS)
        recovered_files = 0
        for i in range(total_attacks):
            recovered_files += 1

    except Exception as e:
        print(e)

    # resume monitoring
    with open("status.txt", "w") as f:
        f.write("running")

    return redirect("/dashboard")
# ---------------- DOWNLOAD LOGS ----------------
@app.route("/download_logs")
def download_logs():
    return send_file("logs/logs.txt", as_attachment=True)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)