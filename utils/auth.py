import streamlit as st

from database.users import (
    register_user,
    login_user
)


# ======================================================
# SESSION
# ======================================================

def initialize_session():

    if "user" not in st.session_state:
        st.session_state.user = None

    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"

    if "reset_mode" not in st.session_state:
        st.session_state.reset_mode = False


# ======================================================
# LOGOUT
# ======================================================

def logout():

    st.session_state.user = None

    # Remove temporary values
    for key in list(st.session_state.keys()):

        if key.startswith("login_") or key.startswith("register_"):
            del st.session_state[key]

    st.rerun()


# ======================================================
# REGISTER PAGE
# ======================================================

def register_page(locations):

    st.subheader("📝 Create Account")

    # ---------------------------------------------------
    # LOCATION SELECTORS (outside the form so they cascade
    # live as the user picks State -> LGA -> Community)
    # ---------------------------------------------------

    state = st.selectbox(
        "State",
        list(locations.keys()),
        key="register_state"
    )

    lga = st.selectbox(
        "Local Government Area",
        list(locations[state].keys()),
        key="register_lga"
    )

    community = st.selectbox(
        "Community",
        locations[state][lga],
        key="register_community"
    )

    with st.form(
        "register_form",
        clear_on_submit=True
    ):

        full_name = st.text_input(
            "Full Name"
        )

        email = st.text_input(
            "Email Address"
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        user_type = st.selectbox(
            "User Type",
            [
                "Crop Farmer",
                "Livestock Farmer",
                "Fish Farmer",
                "Resident"
            ]
        )

        security_question = st.selectbox(
            "Security Question",
            [
                "What was your first school?",
                "What is your favourite crop?",
                "What is your favourite animal?",
                "What town were you born in?",
                "What is your favourite food?",
                "What is your mother's maiden name?"
            ]
        )

        security_answer = st.text_input(
            "Security Answer",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create Account",
            width="stretch"
        )

        if submitted:

            if password != confirm:

                st.error("Passwords do not match.")
                return

            success, message = register_user(
                full_name,
                email,
                username,
                password,
                state,
                lga,
                community,
                user_type,
                security_question,
                security_answer
            )

            if success:

                st.success(message)

                st.info(
                    "You can now login."
                )

                st.session_state.auth_page = "login"

            else:

                st.error(message)


# ======================================================
# LOGIN PAGE
# ======================================================

def login_page():

    st.subheader("🔑 Login")

    with st.form("login_form"):

        identifier = st.text_input(
            "Username or Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Login",
            width="stretch"
        )

        if submitted:

            user = login_user(
                identifier,
                password
            )

            if user:

                st.session_state.user = user

                st.success(
                    f"Welcome {user['full_name']}"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid username/email or password."
                )

    st.markdown("---")

    if st.button(
        "Forgot Password",
        width="stretch"
    ):

        st.session_state.reset_mode = True

        st.rerun()