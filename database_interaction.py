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
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS donation(
            promocode TEXT,
            cash BIGINT
        )""")
        self.clients_db.commit()

    def check_existing_client(self, login):
        self.cursor.execute(f"SELECT login FROM users WHERE login = '{login}' ")
        if self.cursor.fetchone() is None:
            return False
        else:
            return True

    def verify_client(self, password, login):
        self.cursor.execute(
            f"SELECT login FROM users WHERE login = '{login}' and password = '{password}' ")
        if self.cursor.fetchone() is None:
            return False
        else:
            return True

    def register_client(self, password, login):
        if self.check_existing_client(login) == False:
            self.cursor.execute(f"INSERT INTO users VALUES (?,?,?)", (login, password, 100))
            self.clients_db.commit()
            return True
        else:
            return False

    def get_cash(self, login):
        self.cursor.execute(
            f"SELECT cash FROM users WHERE login = '{login}' ")
        cash = self.cursor.fetchone()[0]
        return cash

    def check_promocode(self, promocode, login):
        self.cursor.execute(
            f"SELECT cash FROM donation WHERE promocode = '{promocode}' "
        )

        cash = self.cursor.fetchone()[0]

        self.cursor.execute(
            f"UPDATE users SET cash = cash +{cash} WHERE login = '{login}' "
        )
        self.clients_db.commit()
        return True
