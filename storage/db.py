import sqlite3
import time
class Database:
    def __init__(self, db_name="skillos.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time REAL,
            end_time REAL,
            accuracy REAL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS note_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            expected_note TEXT,
            detected_note TEXT,
            timestamp REAL,
            timing TEXT,
            correct INTEGER
        )
        """)
        self.conn.commit()
    def start_session(self):
        self.start_time = time.time()
        self.cursor.execute("""
        INSERT INTO sessions (start_time)
        VALUES (?)
        """, (self.start_time,))
        self.conn.commit()
        return self.cursor.lastrowid
    def end_session(self, session_id, accuracy):
        end_time = time.time()
        self.cursor.execute("""
        UPDATE sessions
        SET end_time=?, accuracy=?
        WHERE id=?
        """, (end_time, accuracy, session_id))
        self.conn.commit()
    def insert_event(self, session_id, expected, detected, timestamp, timing, correct):
        self.cursor.execute("""
        INSERT INTO note_events 
        (session_id, expected_note, detected_note, timestamp, timing, correct)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (session_id, expected, detected, timestamp, timing, int(correct)))

        self.conn.commit()