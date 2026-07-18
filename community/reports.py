import sqlite3
from datetime import datetime


DATABASE = "database/climate.db"



def add_report(
    user,
    category,
    issue,
    description,
    image
):

    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO reports
        (
        user_id,
        state,
        lga,
        community,
        category,
        issue,
        description,
        image,
        date
        )

        VALUES (?,?,?,?,?,?,?,?,?)

        """,

        (

        user["id"],

        user["state"],

        user["lga"],

        user["community"],

        category,

        issue,

        description,

        image,

        datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        )

    )


    conn.commit()

    conn.close()



def get_reports():

    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM reports
        ORDER BY id DESC
        """
    )


    data = cursor.fetchall()


    conn.close()


    return data