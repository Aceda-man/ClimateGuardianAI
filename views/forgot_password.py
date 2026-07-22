import streamlit as st

from database.users import (
    get_security_question,
    verify_security_answer,
    reset_password
)


def forgot_password_page():

    st.title("🔒 Reset Password")

    st.write(
        "Answer your security question to reset your password."
    )

    # -----------------------------
    # Step 1 - Email
    # -----------------------------
    if "reset_email" not in st.session_state:
        st.session_state.reset_email = ""

    if "security_verified" not in st.session_state:
        st.session_state.security_verified = False

    email = st.text_input(
        "Email Address",
        value=st.session_state.reset_email
    )

    if st.button("Continue"):

        question = get_security_question(email)

        if question is None:

            st.error("No account found with that email.")

            # Clear any stale question/verification from a
            # previous, different email so it can't linger here.
            for key in ["security_question", "security_verified"]:
                st.session_state.pop(key, None)

        else:

            st.session_state.reset_email = email
            st.session_state.security_question = question
            st.rerun()

    # -----------------------------
    # Step 2 - Security Question
    # -----------------------------
    if "security_question" in st.session_state:

        st.divider()

        st.write(
            f"**Security Question:** {st.session_state.security_question}"
        )

        answer = st.text_input(
            "Security Answer",
            type="password"
        )

        if st.button("Verify Answer"):

            if verify_security_answer(
                st.session_state.reset_email,
                answer
            ):

                st.session_state.security_verified = True
                st.success("Security answer verified.")
                st.rerun()

            else:

                st.error("Incorrect security answer.")

    # -----------------------------
    # Step 3 - New Password
    # -----------------------------
    if st.session_state.security_verified:

        st.divider()

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Reset Password"):

            if new_password != confirm_password:

                st.error("Passwords do not match.")

            else:

                success, message = reset_password(
                    st.session_state.reset_email,
                    new_password
                )

                if success:

                    st.success(message)

                    # Clear reset session
                    for key in [
                        "reset_email",
                        "security_question",
                        "security_verified",
                        "reset_mode"
                    ]:
                        st.session_state.pop(key, None)

                    st.info(
                        "You can now login with your new password."
                    )

                    st.rerun()

                else:

                    st.error(message)