import streamlit as st


st.set_page_config(
    page_title="ClimateGuardian AI",
    page_icon="🌍"
)


st.title("🌍 ClimateGuardian AI")

st.subheader(
    "AI-powered Climate Resilience Platform for Nigerian Communities"
)


st.write(
"""
Helping communities prepare for climate risks,
protect livelihoods, and respond to disasters.
"""
)


menu = st.sidebar.selectbox(
    "Navigate",
    [
        "Dashboard",
        "Report Incident",
        "AI Assistant",
        "Community"
    ]
)


if menu == "Dashboard":

    st.header("Community Climate Dashboard")

    st.info(
        "Select a Nigerian location to view climate risk."
    )


elif menu == "Report Incident":

    st.header("Report Climate Incident")

    st.write(
        "Flood, drought, livestock loss, property damage."
    )


elif menu == "AI Assistant":

    st.header("ClimateGuardian Assistant")

    st.write(
        "Gemma AI will be connected here."
    )


elif menu == "Community":

    st.header("Community Reports")

    st.write(
        "Local climate information sharing."
    )