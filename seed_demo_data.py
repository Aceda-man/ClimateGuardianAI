"""
Seed realistic demo data for ClimateGuardian AI.

Run once before your demo:
    python seed_demo_data.py

Safe to re-run: skips creating demo users that already exist
(matched by email), but will add fresh reports/votes/comments
each time it runs, so only run it once per demo session unless
you want to keep piling on data.
"""

from datetime import datetime, timedelta
import random

from database.database import get_connection, create_database
from database.users import hash_text


# ==================================================
# ADJUST THESE to match your actual data/nigeria_locations.json
# spelling if your demo relies on the State/LGA/Community
# dropdowns matching exactly. State/LGA/Community are stored as
# free text (not validated against the JSON), so a mismatch here
# won't break anything -- it just means these demo reports won't
# show up if you filter using different exact names.
# ==================================================

DEMO_USERS = [
    {
        "full_name": "Amara Bello",
        "email": "amara.demo@climateguardian.ai",
        "username": "amara_demo",
        "user_type": "Crop Farmer",
        "state": "Kwara",
        "lga": "Ilorin West",
        "community": "Sango",
    },
    {
        "full_name": "Tunde Afolabi",
        "email": "tunde.demo@climateguardian.ai",
        "username": "tunde_demo",
        "user_type": "Fish Farmer",
        "state": "Kwara",
        "lga": "Ilorin West",
        "community": "Sango",
    },
    {
        "full_name": "Ngozi Chukwu",
        "email": "ngozi.demo@climateguardian.ai",
        "username": "ngozi_demo",
        "user_type": "Livestock Farmer",
        "state": "Kwara",
        "lga": "Ilorin East",
        "community": "Oke Oyi",
    },
    {
        "full_name": "Ibrahim Sule",
        "email": "ibrahim.demo@climateguardian.ai",
        "username": "ibrahim_demo",
        "user_type": "Resident",
        "state": "Kwara",
        "lga": "Ilorin East",
        "community": "Oke Oyi",
    },
    {
        "full_name": "Fatima Yusuf",
        "email": "fatima.demo@climateguardian.ai",
        "username": "fatima_demo",
        "user_type": "Resident",
        "state": "Kwara",
        "lga": "Asa",
        "community": "Afon",
    },
]

DEMO_REPORTS = [
    # (offset_days_ago, incident_type, severity, title, description, author_idx, state/lga/community_idx)
    (6, "Flood", "High", "Flash flooding along Sango market road",
     "Heavy overnight rainfall caused flooding near the market. Several stalls affected.", 0, 0),
    (5, "Drought", "Moderate", "Reduced yield on maize farms near Sango",
     "Extended dry spell affecting maize growth this planting season.", 0, 0),
    (5, "Fish Pond Problem", "High", "Unusual fish deaths in pond cluster",
     "Multiple fish farmers reporting sudden fish deaths, suspected water quality issue.", 1, 0),
    (4, "Crop Disease", "Moderate", "Leaf spot disease spreading in cassava farms",
     "Several farmers noticing similar leaf spotting pattern this week.", 0, 0),
    (4, "Livestock Disease", "Critical", "Suspected outbreak among cattle herd",
     "A number of cattle showing fever and reduced appetite over the last two days.", 2, 1),
    (3, "Erosion", "Moderate", "Gully erosion widening near Oke Oyi road",
     "Erosion channel has grown noticeably after recent rains, close to farmland.", 3, 1),
    (3, "Heatwave", "High", "Extended heatwave affecting livestock",
     "Unusually high daytime temperatures for the past several days.", 2, 1),
    (2, "Water Shortage", "Moderate", "Borehole output reduced in Afon",
     "Community borehole yielding noticeably less water than usual this week.", 4, 2),
    (2, "Pest Infestation", "High", "Armyworm sighting in maize fields",
     "Farmers reporting armyworm damage on young maize plants.", 0, 0),
    (2, "Building Damage", "Low", "Minor roof damage from windstorm",
     "Short but strong windstorm damaged roofing on a few houses.", 3, 1),
    (1, "Road Damage", "Moderate", "Pothole worsening after rainfall",
     "Main road pothole has grown significantly larger after recent rains.", 4, 2),
    (1, "Flood", "Critical", "Rising water levels near Sango stream",
     "Stream levels rising fast, residents near the bank advised to stay alert.", 1, 0),
    (1, "Power Outage", "Low", "Extended outage affecting cold storage",
     "Power has been out for over 24 hours, affecting food storage for farmers.", 2, 1),
    (0, "Crop Disease", "High", "Suspected blight in tomato farms",
     "Rapid wilting observed across several tomato plots today.", 4, 2),
    (0, "Drought", "Low", "Early signs of soil dryness",
     "Soil moisture noticeably lower than usual for this time of year.", 3, 1),
]


def _get_or_create_demo_users(cursor):

    ids = []

    for u in DEMO_USERS:

        cursor.execute(
            "SELECT id FROM users WHERE email=?",
            (u["email"],)
        )
        row = cursor.fetchone()

        if row:
            ids.append(row["id"])
            continue

        cursor.execute(
            """
            INSERT INTO users(
                full_name, email, username, password,
                state, lga, community, user_type,
                security_question, security_answer
            )
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                u["full_name"],
                u["email"],
                u["username"],
                hash_text("DemoPass123!"),
                u["state"],
                u["lga"],
                u["community"],
                u["user_type"],
                "What is your favourite crop?",
                hash_text("demo")
            )
        )

        ids.append(cursor.lastrowid)

    return ids


def seed():

    create_database()

    conn = get_connection()
    cursor = conn.cursor()

    user_ids = _get_or_create_demo_users(cursor)
    conn.commit()

    report_ids = []

    for (days_ago, incident_type, severity, title, description,
         author_idx, loc_idx) in DEMO_REPORTS:

        # locations mirror the 3 distinct areas used above
        loc = [
            {"state": "Kwara", "lga": "Ilorin West", "community": "Sango"},
            {"state": "Kwara", "lga": "Ilorin East", "community": "Oke Oyi"},
            {"state": "Kwara", "lga": "Asa", "community": "Afon"},
        ][loc_idx]

        created_at = (
            datetime.now() - timedelta(
                days=days_ago,
                hours=random.randint(0, 20)
            )
        ).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO reports(
                user_id, incident_type, severity, title, description,
                image_path, state, lga, community, created_at
            )
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                user_ids[author_idx],
                incident_type,
                severity,
                title,
                description,
                None,
                loc["state"],
                loc["lga"],
                loc["community"],
                created_at
            )
        )

        report_ids.append(cursor.lastrowid)

    conn.commit()

    # ----------------------------------------
    # Community verification votes
    # ----------------------------------------

    for report_id in report_ids:

        voters = random.sample(user_ids, k=random.randint(1, 3))

        for voter_id in voters:

            vote = random.choices(
                ["CONFIRM", "FALSE", "UNSURE"],
                weights=[70, 10, 20]
            )[0]

            try:
                cursor.execute(
                    """
                    INSERT INTO report_verifications(report_id, user_id, vote)
                    VALUES(?,?,?)
                    """,
                    (report_id, voter_id, vote)
                )
            except Exception:
                # voter == author or duplicate vote, skip
                pass

    conn.commit()

    # ----------------------------------------
    # A few comments for the Community page
    # ----------------------------------------

    sample_comments = [
        "Seeing the same thing in my area, thanks for flagging this.",
        "Local authorities should be made aware of this urgently.",
        "This matches what my neighbours have been saying too.",
        "Good to know, will keep an eye on it.",
    ]

    for report_id in random.sample(report_ids, k=min(6, len(report_ids))):

        commenter = random.choice(user_ids)

        cursor.execute(
            """
            INSERT INTO comments(report_id, user_id, comment)
            VALUES(?,?,?)
            """,
            (report_id, commenter, random.choice(sample_comments))
        )

    conn.commit()

    # ----------------------------------------
    # Recalculate trust counters from real data
    # so everything is internally consistent
    # ----------------------------------------

    for user_id in user_ids:

        cursor.execute(
            "SELECT COUNT(*) FROM reports WHERE user_id=?",
            (user_id,)
        )
        reports_submitted = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*) FROM report_verifications rv
            JOIN reports r ON rv.report_id = r.id
            WHERE r.user_id=? AND rv.vote='CONFIRM'
            """,
            (user_id,)
        )
        verified = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*) FROM report_verifications rv
            JOIN reports r ON rv.report_id = r.id
            WHERE r.user_id=? AND rv.vote='FALSE'
            """,
            (user_id,)
        )
        false_ct = cursor.fetchone()[0]

        trust_score = max(0, min(100, 50 + (verified * 3) - (false_ct * 5)))

        cursor.execute(
            """
            UPDATE users
            SET reports_submitted=?, verified_reports=?, false_reports=?, trust_score=?
            WHERE id=?
            """,
            (reports_submitted, verified, false_ct, trust_score, user_id)
        )

    conn.commit()
    conn.close()

    print(f"Seeded {len(user_ids)} demo users and {len(report_ids)} reports.")
    print("Demo login: amara.demo@climateguardian.ai / DemoPass123!")


if __name__ == "__main__":
    seed()