import streamlit as st

from database.reports import get_community_feed
from database.verifications import (
    verify_report,
    verification_statistics
)

from database.comments import (
    add_comment,
    get_comments
)

def show_community_page(user):

    st.title("👥 Community Intelligence")

    st.write(
        "Verified reports submitted by members of your community."
    )

    st.divider()

    reports = get_community_feed(
        user["state"],
        user["lga"]
    )

    if len(reports) == 0:

        st.info(
            "No reports have been submitted yet."
        )

        return

    for report in reports:

        with st.container(border=True):

            st.subheader(f"🚨 {report['incident_type']}")

            left, right = st.columns([3, 1])

            with left:

                st.write(f"### {report['title']}")

                st.write(report["description"])

                st.write(
                    f"📍 {report['community']}, {report['lga']}, {report['state']}"
                )

                st.write(
                    f"👤 Reported by **{report['full_name']}**"
                )

            with right:

                severity = report["severity"]

                if severity == "Critical":
                    st.error("🔴 Critical")

                elif severity == "High":
                    st.warning("🟠 High")

                elif severity == "Moderate":
                    st.info("🟡 Moderate")

                else:
                    st.success("🟢 Low")

            if report["image_path"]:

                st.image(
                    report["image_path"],
                    width="stretch"
                )

            st.caption(
                f"🕒 Reported: {report['created_at']}"
            )

            # ====================================
            # COMMUNITY VERIFICATION
            # ====================================

            stats = verification_statistics(
                report["id"]
            )

            st.markdown("### Community Verification")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "✅ Confirm",
                stats["confirm"]
            )

            c2.metric(
                "🚩 False",
                stats["false"]
            )

            c3.metric(
                "❓ Unsure",
                stats["unsure"]
            )

            st.divider()

            b1, b2, b3 = st.columns(3)

            with b1:

                if st.button(
                    "👍 Confirm",
                    key=f"confirm_{report['id']}"
                ):

                    verify_report(
                        report["id"],
                        user["id"],
                        "CONFIRM"
                    )

                    st.success("Thanks for confirming.")

                    st.rerun()

            with b2:

                if st.button(
                    "🚩 False Report",
                    key=f"false_{report['id']}"
                ):

                    verify_report(
                        report["id"],
                        user["id"],
                        "FALSE"
                    )

                    st.warning("Report marked as false.")

                    st.rerun()

            with b3:

                if st.button(
                    "❓ Unsure",
                    key=f"unsure_{report['id']}"
                ):

                    verify_report(
                        report["id"],
                        user["id"],
                        "UNSURE"
                    )

                    st.info("Marked as unsure.")

                    st.rerun()
            st.divider()

            st.subheader("💬 Community Discussion")

            comments = get_comments(report["id"])

            if len(comments) == 0:

                st.caption("No comments yet.")

            else:

                for comment in comments:

                    st.info(
                        f"""
**{comment['full_name']}**

{comment['comment']}

🕒 {comment['created_at']}
"""
                    )

            comment_key = f"comment_{report['id']}"

            new_comment = st.text_area(
                "Write a comment",
                key=comment_key
            )

            if st.button(
                "Post Comment",
                key=f"post_{report['id']}"
            ):

                if new_comment.strip():

                    add_comment(
                        report["id"],
                        user["id"],
                        new_comment
                    )

                    st.success("Comment posted.")

                    # Clear the text box now that the comment is saved,
                    # otherwise the old text lingers after the rerun.
                    del st.session_state[comment_key]

                    st.rerun()