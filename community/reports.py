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

from database.database import get_connection


def get_latest_reports(limit=5):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            reports.id,

            reports.title,

            reports.incident_type,

            reports.severity,

            reports.community,

            reports.created_at,

            users.full_name

        FROM reports

        JOIN users

        ON reports.user_id = users.id

        ORDER BY reports.created_at DESC

        LIMIT ?
        """,
        (limit,)
    )

    reports = cursor.fetchall()

    conn.close()

    return reports