import sqlite3

class DatabaseConnection:
    def __init__(self):
        conn = sqlite3.connect('./database.db')
        self.cursor = conn.cursor()

    def getCursor(self):
        return self.cursor
    