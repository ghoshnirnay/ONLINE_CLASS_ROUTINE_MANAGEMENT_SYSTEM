import os
import sqlite3
import urllib.parse
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
DB_PATH = os.environ.get("CLASSSYNC_DB", "classsync.db")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ---------- DB CONNECTION ----------
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def row(r):
    return {k: r[k] for k in r.keys()}

# ---------- ERROR HANDLER ----------
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "not_found", "message": "Resource not found"}), 404

# ---------- HEALTH ----------
@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

# ---------- AUTH ----------
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json
    name, email, password = data["name"], data["email"], data["password"]
    role = data.get("role", "student")

    con = db(); cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO users(name,email,password_hash,role) VALUES (?,?,?,?)",
            (name, email, generate_password_hash(password), role)
        )
        con.commit()
        return jsonify({"id": cur.lastrowid, "name": name, "email": email, "role": role})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409
    finally:
        con.close()

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    con = db(); cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (data["email"],))
    u = cur.fetchone(); con.close()

    if not u or not check_password_hash(u["password_hash"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    user = row(u)
    del user["password_hash"]
    return jsonify({"user": user})

# ---------- USERS ----------
@app.route("/api/users")
def users():
    role = request.args.get("role")
    con = db(); cur = con.cursor()
    if role:
        cur.execute("SELECT * FROM users WHERE role=?", (role,))
    else:
        cur.execute("SELECT * FROM users")
    rows = [row(r) for r in cur.fetchall()]
    con.close()
    return jsonify(rows)

# ---------- DEPARTMENTS ----------
@app.route("/api/departments")
def departments():
    con = db(); cur = con.cursor()
    cur.execute("SELECT * FROM departments ORDER BY name")
    rows = [row(r) for r in cur.fetchall()]
    con.close()
    return jsonify(rows)

# ---------- SUBJECTS ----------
@app.route("/api/subjects", methods=["GET"])
def subjects():
    con = db(); cur = con.cursor()
    cur.execute("SELECT * FROM subjects ORDER BY name")
    rows = [row(r) for r in cur.fetchall()]
    con.close()
    return jsonify(rows)

@app.route("/api/subjects", methods=["POST"])
def add_subject():
    name = request.json["name"]
    con = db(); cur = con.cursor()
    try:
        cur.execute("INSERT INTO subjects(name) VALUES (?)", (name,))
        con.commit()
        return jsonify({"added": True})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Subject already exists"}), 409
    finally:
        con.close()

@app.route("/api/subjects/<int:id>", methods=["DELETE"])
def delete_subject(id):
    con = db(); cur = con.cursor()
    cur.execute("DELETE FROM subjects WHERE id=?", (id,))
    con.commit(); con.close()
    return jsonify({"deleted": True})

# ---------- FACULTY ↔ SUBJECT ASSIGNMENTS ----------
@app.route("/api/faculty-subjects/<int:faculty_id>", methods=["GET"])
def get_faculty_subjects(faculty_id):
    con = db()
    cur = con.cursor()
    cur.execute("""
        SELECT fs.id, fs.faculty_id, fs.subject_id, s.name AS subject_name
        FROM faculty_subjects fs
        JOIN subjects s ON fs.subject_id = s.id
        WHERE fs.faculty_id = ?
        ORDER BY s.name
    """, (faculty_id,))
    rows = [row(r) for r in cur.fetchall()]
    con.close()
    return jsonify(rows)

@app.route("/api/faculty-subjects", methods=["POST"])
def assign_faculty_subject():
    data = request.get_json()
    faculty_id = data.get("faculty_id")
    subject_id = data.get("subject_id")

    if not faculty_id or not subject_id:
        return jsonify({"error": "Missing faculty_id or subject_id"}), 400

    con = db(); cur = con.cursor()
    try:
        cur.execute("""
            INSERT INTO faculty_subjects (faculty_id, subject_id)
            VALUES (?, ?)
        """, (faculty_id, subject_id))
        con.commit()
        return jsonify({"success": True, "message": "Subject assigned successfully"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "This subject is already assigned to this faculty"}), 409
    finally:
        con.close()

@app.route("/api/faculty-subjects/<int:id>", methods=["DELETE"])
def remove_faculty_subject(id):
    con = db(); cur = con.cursor()
    cur.execute("DELETE FROM faculty_subjects WHERE id = ?", (id,))
    con.commit(); con.close()
    return jsonify({"deleted": True})

# ---------- FIXED FACULTY-BY-SUBJECT ROUTE ----------
@app.route("/api/faculty-by-subject/<string:subject_name>", methods=["GET"])
def get_faculty_by_subject(subject_name):
    """Return only users with role='faculty' teaching the given subject"""
    con = db(); cur = con.cursor()
    cur.execute("""
        SELECT DISTINCT u.id, u.name
        FROM faculty_subjects fs
        JOIN users u ON fs.faculty_id = u.id
        JOIN subjects s ON fs.subject_id = s.id
        WHERE s.name = ? AND u.role = 'faculty'
        ORDER BY u.name
    """, (subject_name,))
    rows = [row(r) for r in cur.fetchall()]
    con.close()
    return jsonify(rows)

# ---------- ROOMS ----------
@app.route("/api/rooms", methods=["GET"])
def get_rooms():
    con = db(); cur = con.cursor()
    cur.execute("SELECT * FROM rooms ORDER BY name")
    rows = [row(r) for r in cur.fetchall()]
    con.close()
    return jsonify(rows)

@app.route("/api/rooms", methods=["POST"])
def add_room():
    d = request.json
    con = db(); cur = con.cursor()
    try:
        cur.execute("INSERT INTO rooms(name,capacity) VALUES (?,?)", (d["name"], d.get("capacity")))
        con.commit()
        return jsonify({"success": True})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Room already exists"}), 409
    finally:
        con.close()

# ---------- TIME SLOTS ----------
@app.route("/api/time-slots", methods=["GET"])
def get_time_slots():
    con = db(); cur = con.cursor()
    cur.execute("SELECT * FROM time_slots ORDER BY start_time")
    rows = [row(r) for r in cur.fetchall()]
    con.close()
    return jsonify(rows)

# ---------- NOTIFICATIONS ----------
def notify_students(cur, department_id, semester, section, message):
    cur.execute("""
        SELECT id FROM users
        WHERE role='student' AND department_id=? AND semester=? AND section=?
    """, (department_id, semester, section))
    for s in cur.fetchall():
        cur.execute("""
            INSERT INTO notifications(user_id, message, created_at)
            VALUES (?, ?, ?)
        """, (s["id"], message, datetime.now().isoformat()))

@app.route("/api/notifications/<int:user_id>")
def get_notifications(user_id):
    con = db(); cur = con.cursor()
    cur.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC", (user_id,))
    rows = [row(r) for r in cur.fetchall()]
    con.close()
    return jsonify(rows)

# ---------- ROUTINES ----------
@app.route("/api/routines", methods=["GET"])
def get_routines():
    args = request.args
    role = args.get("role")
    faculty_name = args.get("name")
    department_id = args.get("department_id")
    semester = args.get("semester")
    section = args.get("section")

    filters, vals = [], []

    # ✅ Student filter
    if role == "student":
        if department_id:
            filters.append("department_id=?"); vals.append(department_id)
        if semester:
            filters.append("semester=?"); vals.append(semester)
        if section:
            filters.append("section=?"); vals.append(section)

    # ✅ Faculty filter
    elif role == "faculty":
        if faculty_name:
            filters.append("faculty_name=?"); vals.append(faculty_name)

    # ✅ Admin/general filter
    else:
        if department_id:
            filters.append("department_id=?"); vals.append(department_id)
        if semester:
            filters.append("semester=?"); vals.append(semester)
        if section:
            filters.append("section=?"); vals.append(section)
        if faculty_name:
            filters.append("faculty_name=?"); vals.append(faculty_name)

    sql = "SELECT * FROM routines"
    if filters:
        sql += " WHERE " + " AND ".join(filters)
    sql += " ORDER BY day, start_time"

    con = db(); cur = con.cursor()
    cur.execute(sql, vals)
    rows = [row(r) for r in cur.fetchall()]
    con.close()
    return jsonify(rows)

# ---------- CREATE ROUTINE (with Optional Faculty + Smart Clash Detection) ----------
@app.route("/api/routines", methods=["POST"])
def create_routine():
    data = request.get_json()
    required = ["department_id", "semester", "section", "day", "subject", "start_time", "end_time"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    department_id = data["department_id"]
    semester = data["semester"]
    section = data["section"]
    day = data["day"]
    subject = data["subject"]
    faculty_name = data.get("faculty_name")
    room = data.get("room")
    start_time = data["start_time"]
    end_time = data["end_time"]

    con = db(); cur = con.cursor()

    # ✅ Smart clash detection (ignore empty faculty)
    query = """
        SELECT * FROM routines
        WHERE day = ?
        AND (
            (
                faculty_name IS NOT NULL AND faculty_name != ''
                AND faculty_name = ?
                AND (? < end_time AND ? > start_time)
            )
            OR
            (
                room IS NOT NULL AND room != ''
                AND room = ?
                AND (? < end_time AND ? > start_time)
            )
        )
    """
    cur.execute(query, (day, faculty_name, start_time, end_time, room, start_time, end_time))
    clash = cur.fetchone()

    if clash:
        con.close()
        return jsonify({"error": "Clash detected! Faculty or Room already assigned during this time."}), 409

    try:
        cur.execute("""
            INSERT INTO routines (department_id, semester, section, day, subject,
                                  faculty_name, room, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            department_id, semester, section, day, subject,
            faculty_name, room, start_time, end_time
        ))
        con.commit()
        return jsonify({"success": True, "message": "Routine created successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Duplicate routine entry"}), 409
    finally:
        con.close()

# ---------- DELETE ROUTINE ----------
@app.route("/api/routines/<int:id>", methods=["DELETE"])
def delete_routine(id):
    con = db(); cur = con.cursor()
    cur.execute("SELECT * FROM routines WHERE id = ?", (id,))
    existing = cur.fetchone()
    if not existing:
        con.close()
        return jsonify({"error": "Routine not found"}), 404

    cur.execute("DELETE FROM routines WHERE id = ?", (id,))
    con.commit()
    con.close()
    return jsonify({"deleted": True, "message": "Routine deleted successfully."}), 200

# ---------- MAIN ----------
if __name__ == "__main__":
    import setup_db
    setup_db.main()
    print("🚀 Server running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
