import pymysql


class Nokubase:
    def __init__(self, settings: dict = {}):

        requirements: list = ["host", "user", "password", "db"]

        for requirement in requirements:
            if not settings.get(requirement):
                raise Exception(f"You're missing a requirement: {requirement}")

        settings["charset"] = (
            settings.get("charset") if settings.get("charset") else "utf8mb4"
        )

        settings["cursorclass"] = (
            settings.get("cursorclass")
            if settings.get("cursorclass")
            else pymysql.cursors.DictCursor
        )

        self.connection = pymysql.connect(**settings)

    def isEmailTaken(self, email: str) -> bool:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT email FROM account WHERE email = %s", (email,))
            result = cursor.fetchone()
            print(result)
            if result:
                return True
            else:
                return False

    def isNickTaken(self, nick: str) -> bool:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT nick FROM account WHERE nick = %s", (nick,))
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False