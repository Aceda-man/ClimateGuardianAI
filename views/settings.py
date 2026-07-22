import streamlit as st

from database.users import (
    update_user_settings,
    update_user_profile
)


def show_settings_page(user, locations):

    st.title("⚙ Settings")

    st.divider()

    st.subheader("Profile")

    st.write(f"**Name:** {user['full_name']}")
    st.write(f"**Email:** {user['email']}")

    st.divider()

    # ==========================================
    # ROLE & LOCATION (reactive, outside any form
    # so State -> LGA -> Community cascades live)
    # ==========================================

    st.subheader("Role & Location")

    st.caption("Update this if you've changed role or moved to a new area.")

    user_type = st.selectbox(
        "User Type",
        [
            "Crop Farmer",
            "Livestock Farmer",
            "Fish Farmer",
            "Resident"
        ],
        index=[
            "Crop Farmer",
            "Livestock Farmer",
            "Fish Farmer",
            "Resident"
        ].index(user["user_type"]),
        key="settings_user_type"
    )

    state = st.selectbox(
        "State",
        list(locations.keys()),
        index=list(locations.keys()).index(user["state"]),
        key="settings_state"
    )

    lga = st.selectbox(
        "Local Government Area",
        list(locations[state].keys()),
        index=list(locations[state].keys()).index(user["lga"])
        if user["lga"] in locations[state] else 0,
        key="settings_lga"
    )

    community = st.selectbox(
        "Community",
        locations[state][lga],
        index=locations[state][lga].index(user["community"])
        if user["community"] in locations[state][lga] else 0,
        key="settings_community"
    )

    if st.button(
        "Save Profile",
        width="stretch",
        key="save_profile"
    ):

        update_user_profile(
            user["id"],
            user_type,
            state,
            lga,
            community
        )

        user["user_type"] = user_type
        user["state"] = state
        user["lga"] = lga
        user["community"] = community
        st.session_state.user = user

        st.success("Profile updated.")

        st.rerun()

    st.divider()

    # ==========================================
    # APPLICATION SETTINGS
    # ==========================================

    st.subheader("Application")

    with st.form("settings_form"):

        dark_mode = st.toggle(
            "Dark Mode",
            value=user.get("dark_mode", False)
        )

        notifications = st.toggle(
            "Notifications",
            value=user.get("notifications", True)
        )

        language = st.selectbox(
            "Language",
            [
                "English",
                "Yoruba",
                "Hausa",
                "Igbo"
            ],
            index=[
                "English",
                "Yoruba",
                "Hausa",
                "Igbo"
            ].index(user.get("language", "English"))
        )

        saved = st.form_submit_button(
            "Save Settings",
            width="stretch"
        )

    if saved:

        update_user_settings(
            user["id"],
            dark_mode,
            notifications,
            language
        )

        user["dark_mode"] = dark_mode
        user["notifications"] = notifications
        user["language"] = language
        st.session_state.user = user

        st.success("Settings saved.")

    st.divider()

    st.info(
        "Additional settings will be added in future versions."
    )