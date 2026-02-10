from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "database.db"

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY,
            agent TEXT,
            file TEXT,
            change TEXT,
            severity TEXT,
            mitre TEXT,
            time TEXT
        )
        """)

def severity(file):
    if "HKCU" in file:
        return "HIGH"
    if "monitored" in file:
        return "MEDIUM"
    return "LOW"


def mitre(file):
    if "Run" in file or "RunOnce" in file:
        return "T1547"  # Boot or Logon Autostart Execution
    if "passwd" in file:
        return "T1548"
    return "T1083"


@app.route("/api/alert", methods=["POST"])
def alert():
    data = request.json

    with sqlite3.connect(DB) as con:
        con.execute(
            "INSERT INTO alerts VALUES (NULL,?,?,?,?,?,?)",
            (
                data["agent_id"],
                data["file"],
                data["change"],
                severity(data["file"]),
                mitre(data["file"]),
                data["timestamp"]
            )
        )

    return jsonify({"status": "stored"}), 201

@app.route("/")
def dashboard():
    with sqlite3.connect(DB) as con:
        rows = con.execute("SELECT * FROM alerts ORDER BY id DESC").fetchall()

    return render_template("dashboard.html", alerts=rows)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
