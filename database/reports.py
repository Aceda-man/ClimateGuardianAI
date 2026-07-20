import sqlite3
from database.database import get_connection


# ============================================
# CREATE REPORT
# ============================================

def create_report(
    user_id,
    incident_type,
    severity,
    title,
    description,
    image_path,
    state,
    lga,
    community
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reports(

            user_id,
            incident_type,
            severity,
            title,
            description,
            image_path,
            state,
            lga,
            community

        )

        VALUES(?,?,?,?,?,?,?,?,?)

        """,
        (
            user_id,
            incident_type,
            severity,
            title,
            description,
            image_path,
            state,
            lga,
            community
        )
    )

    conn.commit()
    conn.close()


# ============================================
# ALL REPORTS
# ============================================

def get_all_reports():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            reports.*,
            users.full_name

        FROM reports

        JOIN users

        ON reports.user_id = users.id

        ORDER BY created_at DESC

    """)

    reports = cursor.fetchall()

    conn.close()

    return reports


# ============================================
# USER REPORTS
# ============================================

def get_user_reports(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """

        SELECT *

        FROM reports

        WHERE user_id=?

        ORDER BY created_at DESC

        """,
        (user_id,)
    )

    reports = cursor.fetchall()

    conn.close()

    return reports


# ============================================
# COMMUNITY REPORTS
# ============================================

def get_community_reports(state, lga):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """

        SELECT
            reports.*,
            users.full_name

        FROM reports

        JOIN users

        ON reports.user_id = users.id

        WHERE
            reports.state=?
        AND
            reports.lga=?

        ORDER BY created_at DESC

        """,
        (
            state,
            lga
        )
    )

    reports = cursor.fetchall()

    conn.close()

    return reports

def report_statistics():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reports")
    total_reports = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM reports
        WHERE severity='Critical'
        """
    )

    critical_reports = cursor.fetchone()[0]

    conn.close()

    return {
        "total_reports": total_reports,
        "critical_reports": critical_reports
    }

# ============================================
# COMMUNITY FEED
# ============================================

def get_community_feed(state, lga):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            reports.*,
            users.full_name

        FROM reports

        JOIN users
            ON reports.user_id = users.id

        WHERE
            reports.state = ?
            AND reports.lga = ?

        ORDER BY reports.created_at DESC
        """,
        (
            state,
            lga
        )
    )

    reports = cursor.fetchall()

    conn.close()

    return reports

# ============================================
# LATEST REPORTS
# ============================================

def get_latest_reports(limit=5):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            reports.*,
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

    # ============================================
# REPORTS BY SEVERITY
# ============================================

def reports_by_severity():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT severity, COUNT(*) as total
        FROM reports
        GROUP BY severity
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ============================================
# REPORTS BY INCIDENT TYPE
# ============================================

def reports_by_type():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT incident_type, COUNT(*) as total
        FROM reports
        GROUP BY incident_type
        ORDER BY total DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data