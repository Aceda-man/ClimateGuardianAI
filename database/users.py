import sqlite3


DATABASE = "database/climate.db"


def add_user(
    name,
    password,
    state,
    lga,
    community,
    user_type
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO users
        (
        name,
        password,
        state,
        lga,
        community,
        user_type
        )

        VALUES (?,?,?,?,?,?)
        """,

        (
            name,
            password,
            state,
            lga,
            community,
            user_type
        )
    )


    conn.commit()
    conn.close()



def login_user(name, password):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE name=? AND password=?
        """,
        (
            name,
            password
        )
    )


    user = cursor.fetchone()

    conn.close()


    return user