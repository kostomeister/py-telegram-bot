import sqlite3


class Database:
    def __init__(self, db_path="bot_database.sqlite3"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            location TEXT,
            checklist TEXT,
            comment TEXT,
            photo_url TEXT NULL 
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_report(
        self, user_id, location, checklist, comment="Все чисто", photo_url=None
    ):
        query = """
        INSERT INTO reports (user_id, location, checklist, comment, photo_url)
        VALUES (?, ?, ?, ?, ?);
        """
        self.conn.execute(query, (user_id, location, checklist, comment, photo_url))
        self.conn.commit()

    def get_existing_reports(self, user_id, location):
        query = """
        SELECT *
        FROM reports
        WHERE user_id = ? AND location = ?
        ORDER BY id DESC;
        """
        cursor = self.conn.execute(query, (user_id, location))
        results = cursor.fetchall()

        reports = []
        for result in results:
            report = {
                "id": result[0],
                "user_id": result[1],
                "location": result[2],
                "checklist": result[3],
                "comment": result[4],
                "photo_url": result[5],
            }
            reports.append(report)

        return reports if reports else None

    def close_connection(self):
        self.conn.close()


db = Database()
