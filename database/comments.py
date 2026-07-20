from database.database import get_connection


def add_comment(report_id, user_id, comment):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO comments(
            report_id,
            user_id,
            comment
        )
        VALUES(?,?,?)
        """,
        (
            report_id,
            user_id,
            comment
        )
    )

    conn.commit()
    conn.close()


def get_comments(report_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            comments.*,
            users.full_name
        FROM comments
        JOIN users
        ON comments.user_id = users.id
        WHERE report_id=?
        ORDER BY created_at DESC
        """,
        (report_id,)
    )

    comments = cursor.fetchall()

    conn.close()

    return comments