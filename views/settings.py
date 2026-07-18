import streamlit as st


def show_settings_page(user):

    st.title("⚙ Settings")

    st.divider()

    st.subheader("Profile")

    st.write(f"**Name:** {user['name']}")
    st.write(f"**Role:** {user['user_type']}")
    st.write(f"**Email:** {user['email']}")
    st.write(
        f"**Location:** {user['community']}, {user['lga']}, {user['state']}"
    )

    st.divider()

    st.subheader("Application")

    dark_mode = st.toggle(
        "Dark Mode",
        value=False
    )

    notifications = st.toggle(
        "Notifications",
        value=True
    )

    language = st.selectbox(
        "Language",
        [
            "English",
            "Yoruba",
            "Hausa",
            "Igbo"
        ]
    )

    st.divider()

    st.info(
        "Additional settings will be added in future versions."
    )