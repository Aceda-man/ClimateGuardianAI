import streamlit as st

from database.users import (
    get_security_question,
    verify_security_answer,
    reset_password
)


def forgot_password_page():

    st.title("🔒 Reset Password")

    # -------------------------------
    # Session Variables
    # -------------------------------
    if "reset_email" not in st.session_state:
        st.session_state.reset_email = ""

    if "question_loaded" not in st.session_state:
        st.session_state.question_loaded = False

    # -------------------------------
    # Step 1
    # -------------------------------
    if not st.session_state.question_loaded:

        with st.form("email_form"):

            email = st.text_input("Enter your registered Email")

            submit = st.form_submit_button("Continue")

            if submit:

                question = get_security_question(email)

                if question:

                    st.session_state.reset_email = email
                    st.session_state.security_question = question
                    st.session_state.question_loaded = True

                    st.rerun()

                else:

                    st.error("No account found with that email.")

    # -------------------------------
    # Step 2
    # -------------------------------
    else:

        st.info(st.session_state.security_question)

        with st.form("reset_form"):

            answer = st.text_input(
                "Security Answer",
                type="password"
            )

            new_password = st.text_input(
                "New Password",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            submit = st.form_submit_button(
                "Reset Password"
            )

            if submit:

                if new_password != confirm_password:

                    st.error("Passwords do not match.")

                elif not verify_security_answer(
                    st.session_state.reset_email,
                    answer
                ):

                    st.error("Incorrect security answer.")

                else:

                    success, message = reset_password(
                        st.session_state.reset_email,
                        new_password
                    )

                    if success:

                        st.success(message)

                        st.session_state.question_loaded = False
                        st.session_state.reset_email = ""

                    else:

                        st.error(message)