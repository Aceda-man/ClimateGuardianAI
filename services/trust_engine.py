from database.database import get_connection


def update_trust_score(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            reports_submitted,
            verified_reports,
            false_reports
        FROM users
        WHERE id=?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    if user is None:
        conn.close()
        return

    score = 50

    score += user["verified_reports"] * 3
    score -= user["false_reports"] * 5

    score = max(0, min(score, 100))

    cursor.execute(
        """
        UPDATE users
        SET trust_score=?
        WHERE id=?
        """,
        (score, user_id)
    )

    conn.commit()
    conn.close()


def get_badge(score):

    if score >= 90:
        return "🏆 Community Champion"

    elif score >= 75:
        return "⭐ Trusted Reporter"

    elif score >= 50:
        return "✅ Community Member"

    elif score >= 25:
        return "🟡 New Reporter"

    else:
        return "🔴 Needs Verification"