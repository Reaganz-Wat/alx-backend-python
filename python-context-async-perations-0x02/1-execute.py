import sqlite3


class ExecuteQuery():
    def __init__(self, query, parameter):
        self.query = query
        self.parameter = parameter
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = sqlite3.connect('../python-decorators-0x01/users.db')
            self.cursor = self.connection.cursor()
            results = self.cursor.execute(self.query, (self.parameter,)).fetchall()
            return results
        except Exception as e:
            print(f"Exception: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
        return True

print(f"...........START OF FILE..............\n")
with ExecuteQuery("SELECT * FROM users WHERE age > ?", 25) as result:
    print(result)

print(f"\n.............END OF FILE................")