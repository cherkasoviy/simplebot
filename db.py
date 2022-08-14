import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS history(
                                                                        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                        timestamp TEXT,
                                                                        user_id TEXT,
                                                                        direction TEXT,
                                                                        text TEXT,
                                                                        data TEXT);
                                                                    """)
        self.connection.commit()

    def add(self, user_id, direction, text, data):
        with self.connection:
            return self.cursor.execute(
                'INSERT INTO history (timestamp, user_id, direction, text, data) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)', (
                                                 user_id, direction, text, data))
