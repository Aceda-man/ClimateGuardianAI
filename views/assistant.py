import streamlit as st


def show_assistant_page(user):

    st.title("🤖 ClimateGuardian AI")

    st.caption("Offline AI Assistant")

    st.divider()

    st.write(
        f"""
Hello **{user['full_name']}** 👋

How can I help you today?
"""
    )

    prompt = st.text_area(
        "Ask ClimateGuardian AI"
    )

    if st.button("Ask AI", type="primary"):

        st.info(
            """
Gemma integration will be connected here.

For now this page serves as the placeholder
for your offline AI assistant.
"""
        )