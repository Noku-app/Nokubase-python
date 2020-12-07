import pymysql

class Nokubase:
    def __init__(self, settings={}):

        requirements = [
            "host",
            "user",
            "password",
            "db"
        ]

        for requirement in requirements:
            if not settings.get(requirement):
                raise Exception("You're missing a requirement: " + requirement)

        settings["charset"] = settings.get("charset") if settings.get("charset") else "utf8mb4"

        settings["cursorclass"] = settings.get("cursorclass") if settings.get("cursorclass") else pymysql.cursors.DictCursor

        self.connection = pymysql.connect(**settings)

    def isEmailTaken(self, email):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT email FROM registered WHERE email = %s",
                (
                    email,
                )
            )
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
