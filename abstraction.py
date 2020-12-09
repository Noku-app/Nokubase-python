import pymysql, time

creates = [
    """CREATE TABLE IF NOT EXISTS tokens 
    (
        uid INT UNSIGNED NOT NULL, 
        secret VARCHAR(60) NOT NULL, 
        token VARCHAR(150) NOT NULL
    );""", 

    """CREATE TABLE IF NOT EXISTS account 
    (
        uid INT UNSIGNED NOT NULL, 
        email VARCHAR(50) NOT NULL, 
        creation_time BIGINT UNSIGNED NOT NULL,
        points INT UNSIGNED NOT NULL,
        pfp VARCHAR(60),
        age INT UNSIGNED,
        nsfw BOOLEAN NOT NULL,
        moderator BOOLEAN NOT NULL,
        admin BOOLEAN NOT NULL,
        developer BOOLEAN NOT NULL,
        gender VARCHAR(8),
        nick VARCHAR(20) NOT NULL,
        bio VARCHAR(500),
        background_color VARCHAR(10),
        border_color VARCHAR(10)
    );"""
]


class Nokubase:
    def __init__(self, settings: dict = {}):

        requirements: list = ["host", "user", "password", "db"]

        clear = settings["clear"] if settings["clear"] else False
        settings.pop("clear") if settings.get("clear") else False

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

        if clear:
            with self.connection.cursor() as cursor:
                for cleanee in creates:
                    cursor.execute(cleanee)

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

    def registerUser(self, options):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ACCOUNT
                (email, uid, creation_time, points, pfp, age, nsfw, moderator, admin, developer, gender, nick, bio, background_color, border_color)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    options.get("email"),
                    options.get("uid"),
                    options["creation_time"] if options.get("creation_time") else time.time() * 1000,
                    options["points"] if options.get("points") else 0,
                    options["pfp"] if options.get("pfp") else None,
                    options["age"] if options.get("age") else None,
                    options["nsfw"] if options.get("nswf") else False,
                    options["moderator"] if options.get("moderator") else False,
                    options["admin"] if options.get("admin") else False,
                    options["developer"] if options.get("developer") else False,
                    options["gender"] if options.get("gender") else None,
                    options["nick"],
                    options["bio"] if options.get("bio") else None,
                    options["background_color"] if options.get("background_color") else None,
                    options["border_color"] if options.get("border_color") else None
                ]
            )
    
    def tokenUser(self, uid, secret, token):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO TOKENS (uid, secret, token) VALUES (?, ?, ?)",
                [
                    uid,
                    secret,
                    token
                ]
            )

    def updateSecret(self, uid, secret):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE tokens SET secret = ? WHERE uid = ?",
                [
                    secret, 
                    uid
                ]
            )

    def updateToken(self, uid, token):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UDPATE tokens SET token = ? WHERE uid = ?", 
                [
                    token, 
                    uid
                ]
            )


            