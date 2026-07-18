import streamlit as st

from database.reports import get_community_feed


def show_community_page(user):

    st.title("👥 Community Intelligence")

    st.write(
        "Reports submitted by members of your community."
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

            st.subheader(
                f"🚨 {report['incident_type']}"
            )

            left, right = st.columns([3, 1])

            with left:

                st.write(f"**Title:** {report['title']}")

                st.write(
                    f"**Description:** {report['description']}"
                )

                st.write(
                    f"📍 {report['community']}, {report['lga']}"
                )

                st.write(
                    f"👤 Reported by: {report['full_name']}"
                )

            with right:

                severity = report["severity"]

                if severity == "Critical":
                    st.error(severity)

                elif severity == "High":
                    st.warning(severity)

                elif severity == "Moderate":
                    st.info(severity)

                else:
                    st.success(severity)

            if report["image_path"]:

                st.image(
                    report["image_path"],
                    use_container_width=True
                )

            st.caption(
                f"Reported: {report['created_at']}"
            )

            st.markdown("---")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.button(
                    "👍 Confirm",
                    key=f"confirm_{report['id']}"
                )

            with col2:

                st.button(
                    "⚠ Flag",
                    key=f"flag_{report['id']}"
                )

            with col3:

                st.button(
                    "💬 Comment",
                    key=f"comment_{report['id']}"
                )