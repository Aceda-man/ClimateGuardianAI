from database.database import get_connection


def verify_report(report_id, user_id, vote):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT id

    FROM report_verifications

    WHERE report_id=?

    AND user_id=?

    """,(report_id,user_id))

    existing = cursor.fetchone()

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

    conn.commit()

    conn.close()


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