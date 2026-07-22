from database.database import get_connection
from services.trust_engine import update_trust_score


def _get_report_owner(cursor, report_id):

    cursor.execute(
        "SELECT user_id FROM reports WHERE id=?",
        (report_id,)
    )

    row = cursor.fetchone()

    return row["user_id"] if row else None


def _adjust_owner_counters(cursor, owner_id, old_vote, new_vote):

    # Only CONFIRM and FALSE affect trust score; UNSURE does not.
    if old_vote == new_vote:
        return

    if old_vote == "CONFIRM":
        cursor.execute(
            "UPDATE users SET verified_reports = verified_reports - 1 WHERE id=?",
            (owner_id,)
        )

    elif old_vote == "FALSE":
        cursor.execute(
            "UPDATE users SET false_reports = false_reports - 1 WHERE id=?",
            (owner_id,)
        )

    if new_vote == "CONFIRM":
        cursor.execute(
            "UPDATE users SET verified_reports = verified_reports + 1 WHERE id=?",
            (owner_id,)
        )

    elif new_vote == "FALSE":
        cursor.execute(
            "UPDATE users SET false_reports = false_reports + 1 WHERE id=?",
            (owner_id,)
        )


def verify_report(report_id, user_id, vote):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT id, vote

    FROM report_verifications

    WHERE report_id=?

    AND user_id=?

    """,(report_id,user_id))

    existing = cursor.fetchone()

    old_vote = existing["vote"] if existing else None

    if existing:

        cursor.execute("""

        UPDATE report_verifications

        SET vote=?

        WHERE id=?

        """,(vote,existing["id"]))

    else:

        cursor.execute("""

        INSERT INTO report_verifications(

            report_id,

            user_id,

            vote

        )

        VALUES(?,?,?)

        """,(report_id,user_id,vote))

    owner_id = _get_report_owner(cursor, report_id)

    if owner_id is not None:
        _adjust_owner_counters(cursor, owner_id, old_vote, vote)

    conn.commit()

    conn.close()

    # Recalculate the report owner's trust score from the fresh counts.
    if owner_id is not None:
        update_trust_score(owner_id)


def verification_statistics(report_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT COUNT(*)

    FROM report_verifications

    WHERE report_id=?

    AND vote='CONFIRM'

    """,(report_id,))

    confirms = cursor.fetchone()[0]

    cursor.execute("""

    SELECT COUNT(*)

    FROM report_verifications

    WHERE report_id=?

    AND vote='FALSE'

    """,(report_id,))

    false_reports = cursor.fetchone()[0]

    cursor.execute("""

    SELECT COUNT(*)

    FROM report_verifications

    WHERE report_id=?

    AND vote='UNSURE'

    """,(report_id,))

    unsure = cursor.fetchone()[0]

    conn.close()

    return {

        "confirm": confirms,

        "false": false_reports,

        "unsure": unsure

    }