import sqlite3
import os

DB_PATH = os.environ.get("CLASSSYNC_DB", "classsync.db")

schema = '''
PRAGMA foreign_keys = ON;

-- 🧑‍💻 USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin','faculty','student')),
    department_id INTEGER,
    semester INTEGER,
    section TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);

-- 🏫 DEPARTMENTS TABLE
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- 📘 SUBJECTS TABLE
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- 🧑‍🏫 FACULTY ↔ SUBJECT LINK TABLE
CREATE TABLE IF NOT EXISTS faculty_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    FOREIGN KEY(faculty_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    UNIQUE(faculty_id, subject_id)
);

-- 🏠 ROOMS TABLE
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    capacity INTEGER
);

-- ⏰ TIME SLOTS TABLE
CREATE TABLE IF NOT EXISTS time_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    UNIQUE(start_time, end_time)
);

-- 🗓️ CLASS ROUTINES TABLE
CREATE TABLE IF NOT EXISTS routines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_id INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    section TEXT NOT NULL,
    day TEXT NOT NULL,
    subject TEXT NOT NULL,
    room TEXT,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    faculty_name TEXT,
    FOREIGN KEY(department_id) REFERENCES departments(id) ON DELETE CASCADE
);

-- 🔔 NOTIFICATIONS TABLE
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 🔄 FACULTY ↔ FACULTY CLASS SWAP REQUESTS
CREATE TABLE IF NOT EXISTS swap_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_name TEXT NOT NULL,
    swap_with_faculty TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    subject TEXT,
    section TEXT,
    swap_with_section TEXT,
    routine_id INTEGER,
    swap_with_routine_id INTEGER,
    status TEXT DEFAULT 'Pending',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (routine_id) REFERENCES routines(id) ON DELETE CASCADE,
    FOREIGN KEY (swap_with_routine_id) REFERENCES routines(id) ON DELETE CASCADE
);
'''

# ✅ Default Department Seeds
seed_data = '''
INSERT OR IGNORE INTO departments(name) VALUES
 ('CSE'), ('ECE'), ('EEE'), ('IT'), ('ME');
'''

def main():
    print("🧩 Initializing ClassSync database...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        conn.executescript(schema)
        conn.executescript(seed_data)
        conn.commit()

        # Quick schema validation
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cur.fetchall()]
        print("✅ Tables created:", tables)

        # Optional: ensure default departments exist
        cur.execute("SELECT COUNT(*) FROM departments;")
        count = cur.fetchone()[0]
        print(f"✅ Department entries: {count}")

        print(f"\n🎯 SQLite DB initialized successfully at: {DB_PATH}")

    except Exception as e:
        print("❌ Error during setup:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
