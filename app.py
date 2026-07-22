import streamlit as st

from utils.helpers import load_locations
from utils.auth import (
    initialize_session,
    register_page,
    login_page,
    logout
)

from views.forgot_password import forgot_password_page

from views.dashboard import show_dashboard
from views.report import show_report_page
from views.community import show_community_page
from views.assistant import show_assistant_page
from views.settings import show_settings_page


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="ClimateGuardian AI",
    page_icon="🌍",
    layout="wide"
)

initialize_session()

locations = load_locations()


# ===================================================
# LANDING PAGE (NOT LOGGED IN)
# ===================================================

if st.session_state.user is None:

    left, right = st.columns([1.7, 1])

    # ---------------- LEFT SIDE ----------------

    with left:

        st.title("🌍 ClimateGuardian AI")

        st.subheader("Community Climate Intelligence")

        st.markdown(
            """
### Community Climate Intelligence for Resilient Cities

ClimateGuardian AI helps communities detect, report and respond to
climate and environmental hazards early — turning ground-level
reports into real-time risk intelligence and safety advisories.
Every report shared strengthens early warning for the whole
community and reduces exposure to preventable climate loss.

### Who can use ClimateGuardian AI?

🌱 Crop Farmers

🐄 Livestock Farmers

🐟 Fish Farmers

🏠 Community Residents

---

### Features

✅ Community Incident Reporting

✅ Live Community Risk Monitoring

✅ Government-Style Safety Advisories

✅ Offline AI Assistant (Gemma) for on-device guidance

✅ Community-Verified Reporting & Trust Scoring

---

*"Building Climate-Resilient Communities Across Nigeria."*
"""
        )

    # ---------------- RIGHT SIDE ----------------

    with right:

        # ---------------- RESET PASSWORD ----------------

        if st.session_state.reset_mode:

            forgot_password_page()

            st.divider()

            if st.button(
                "⬅ Back to Login",
                use_container_width=True
            ):

                st.session_state.reset_mode = False

                for key in [
                    "reset_email",
                    "security_question",
                    "security_verified"
                ]:
                    st.session_state.pop(key, None)

                st.rerun()

        # ---------------- LOGIN / REGISTER ----------------

        else:

            st.markdown("## Welcome")

            auth = st.radio(
                "",
                ["Login", "Create Account"],
                horizontal=True,
                key="landing_auth"
            )

            st.divider()

            if auth == "Login":
                login_page()

            else:
                register_page(locations)


# ===================================================
# USER LOGGED IN
# ===================================================

else:

    user = st.session_state.user

    st.sidebar.title("🌍 ClimateGuardian AI")
    st.sidebar.caption("Community Climate Intelligence")

    st.sidebar.divider()

    st.sidebar.success(f"👤 {user['full_name']}")

    st.sidebar.write(f"📍 {user['community']}")
    st.sidebar.write(f"🏙 {user['lga']}, {user['state']}")
    st.sidebar.write(f"🌾 {user['user_type']}")

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Report Incident",
            "Community",
            "AI Assistant",
            "Settings"
        ],
        key="navigation"
    )

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout"):
        logout()

    if page == "Dashboard":
        show_dashboard(user)

    elif page == "Report Incident":
        show_report_page(user)

    elif page == "Community":
        show_community_page(user)

    elif page == "AI Assistant":
        show_assistant_page(user)

    elif page == "Settings":
        show_settings_page(user, locations)