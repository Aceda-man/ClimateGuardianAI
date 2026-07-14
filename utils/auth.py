import streamlit as st

from database.users import add_user, login_user


def initialize_session():

    if "user" not in st.session_state:
        st.session_state.user = None



def register_page(locations):

    st.title("🌍 Create ClimateGuardian Profile")


    name = st.text_input(
        "Full Name"
    )


    password = st.text_input(
        "Create Password",
        type="password"
    )


    state = st.selectbox(
        "State",
        list(locations.keys())
    )


    lga = st.selectbox(
        "Local Government Area",
        list(locations[state].keys())
    )


    community = st.selectbox(
        "Community",
        locations[state][lga]
    )


    user_type = st.radio(
        "You are a:",
        [
            "Crop Farmer",
            "Livestock Farmer",
            "Fish Farmer",
            "Resident"
        ]
    )


    if st.button(
        "Create Account"
    ):

        add_user(
            name,
            password,
            state,
            lga,
            community,
            user_type
        )


        st.success(
            "Account created. Please login."
        )



def login_page():

    st.title(
        "🌍 Login to ClimateGuardian"
    )


    name = st.text_input(
        "Name"
    )


    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button(
        "Login"
    ):

        user = login_user(
            name,
            password
        )


        if user:

            st.session_state.user = {

                "id": user[0],
                "name": user[1],
                "state": user[3],
                "lga": user[4],
                "community": user[5],
                "user_type": user[6]

            }


            st.success(
                "Login successful"
            )

            st.rerun()


        else:

            st.error(
                "Invalid login details"
            )