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
        self.cursor.execute(f"SELECT login FROM users WHERE login = '{login}' ")
        if self.cursor.fetchone() is None:
            return False
        else:
            return True

    def verify_client(self):
        pass

    def register_client(self, password, login):
        if self.check_existing_client(login) == False:
            self.cursor.execute(f"INSERT INTO users VALUES (?,?,?)", (login, password, 100))
            self.clients_db.commit()
            return True
        else:
            return False
