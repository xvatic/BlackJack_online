import sqlite3


class Users():
    def __init__(self):
        self.clients_db = sqlite3.connect("clientdatabase.db")
        self.cursor = self.clients_db.cursor()

    def check_database_existing(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            login TEXT,
            password TEXT,
            cash BIGINT
        )""")
        self.clients_db.commit()

    def check_existing_client(login):
        pass

    def verify_client(self):
        pass

    def register_client(self, password, login):
        self.check_existing_client(login)
