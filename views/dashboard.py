import streamlit as st

from database.reports import report_statistics


def show_dashboard(user):

    stats = report_statistics()

    st.title("🌍 ClimateGuardian AI")

    st.subheader(f"Welcome back, {user['full_name']} 👋")

    st.write(
        "Monitor climate risks, community reports and environmental conditions in your area."
    )

    st.divider()

    # =====================================
    # QUICK STATISTICS
    # =====================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🚨 Total Reports",
            stats["total_reports"]
        )

    with col2:
        st.metric(
            "🔴 Critical Reports",
            stats["critical_reports"]
        )

    with col3:
        st.metric(
            "🌧 Flood Risk",
            "Low"
        )

    with col4:
        st.metric(
            "🤖 AI Status",
            "Offline"
        )

    st.divider()

    left, right = st.columns([2, 1])

    # =====================================
    # LEFT COLUMN
    # =====================================

    with left:

        st.subheader("📢 Community Situation")

        if stats["total_reports"] == 0:

            st.success(
                "No incidents have been reported in your community."
            )

        else:

            st.warning(
                f"There are currently **{stats['total_reports']}** reported incidents."
            )

            if stats["critical_reports"] > 0:

                st.error(
                    f"⚠ {stats['critical_reports']} report(s) are marked as CRITICAL."
                )

        st.divider()

        st.subheader("📰 Community Updates")

        st.info(
            """
Reports submitted by residents will appear here.

In the next stage this section will display:

• Latest reports

• Images

• AI summaries

• Community verification

• Time of report
"""
        )

    # =====================================
    # RIGHT COLUMN
    # =====================================

    with right:

        st.subheader("👤 My Profile")

        st.write(f"**Name:** {user['full_name']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Role:** {user['user_type']}")
        st.write(f"**State:** {user['state']}")
        st.write(f"**LGA:** {user['lga']}")
        st.write(f"**Community:** {user['community']}")

        st.divider()

        st.subheader("🤖 Gemma AI")

        st.warning("Offline")

        st.caption(
            "Gemma will analyze reports during the hackathon."
        )