import streamlit as st

from utils.helpers import load_locations
from utils.auth import (
    initialize_session,
    register_page,
    login_page
)


st.set_page_config(
    page_title="ClimateGuardian AI",
    page_icon="🌍"
)


initialize_session()

locations = load_locations()


if st.session_state.user is None:


    choice = st.radio(
        "Welcome to ClimateGuardian AI",
        [
            "Register",
            "Login"
        ]
    )


    if choice == "Register":

        register_page(
            locations
        )


    else:

        login_page()



else:


    user = st.session_state.user


    st.title(
        "🌍 ClimateGuardian AI"
    )


    st.write(
        f"""
        Welcome {user['name']} 👋

        📍 {user['community']},
        {user['lga']},
        {user['state']}

        👤 {user['user_type']}
        """
    )


    page = st.radio(
        "Navigate",
        [
            "Dashboard",
            "Report Incident",
            "AI Assistant",
            "Community"
        ]
    )


    if page == "Dashboard":

        st.header(
            "Climate Dashboard"
        )


        st.info(
            "Climate monitoring will appear here."
        )


    elif page == "Report Incident":

        st.header(
            "Report Climate Incident"
        )


    elif page == "AI Assistant":

        st.header(
            "Gemma AI Assistant"
        )


    elif page == "Community":

        st.header(
            "Community Dashboard"
        )