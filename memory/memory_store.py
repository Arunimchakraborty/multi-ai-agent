import sqlite3
import json
import time

class MemoryStore:
    def __init__(self, db_path="memory_store.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS memory_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                source TEXT,
                format TEXT,
                intent TEXT
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS context (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.conn.commit()

    def log_entry(self, entry: dict):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO memory_log (timestamp, source, format, intent)
            VALUES (?, ?, ?, ?)
        ''', (
            time.time(),
            entry.get("source", "unknown"),
            entry.get("format", "unknown"),
            entry.get("intent", "unknown")
        ))
        self.conn.commit()

    def update_context(self, data: dict):
        cur = self.conn.cursor()
        for k, v in data.items():
            cur.execute('''
                INSERT INTO context (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            ''', (k, json.dumps(v)))
        self.conn.commit()

    def get_context(self):
        cur = self.conn.cursor()
        cur.execute('SELECT key, value FROM context')
        rows = cur.fetchall()
        return {k: json.loads(v) for k, v in rows}

    def get_logs(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM memory_log ORDER BY timestamp DESC')
        rows = cur.fetchall()
        return [
            {
                "id": row[0],
                "timestamp": row[1],
                "source": row[2],
                "format": row[3],
                "intent": row[4]
            } for row in rows
        ]
