import os
from pathlib import Path

import streamlit as st

from database.reports import create_report


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def show_report_page(user):

    st.title("📢 Report Incident")

    st.write(
        "Report a climate, environmental or agricultural incident in your community."
    )

    st.divider()

    with st.form("report_form", clear_on_submit=True):

        incident_type = st.selectbox(
            "Incident Type",
            [
                "Flood",
                "Wildfire",
                "Heatwave",
                "Drought",
                "Erosion",
                "Crop Disease",
                "Livestock Disease",
                "Fish Pond Problem",
                "Building Damage",
                "Road Damage",
                "Power Outage",
                "Water Shortage",
                "Pest Infestation",
                "Other"
            ]
        )

        severity = st.select_slider(
            "Severity",
            options=[
                "Low",
                "Moderate",
                "High",
                "Critical"
            ]
        )

        title = st.text_input(
            "Incident Title"
        )

        description = st.text_area(
            "Describe what happened"
        )

        image = st.file_uploader(
            "Upload Evidence (Optional)",
            type=["jpg", "jpeg", "png"]
        )

        st.markdown("### 📍 Report Location")

        st.info(f"State: {user['state']}")
        st.info(f"LGA: {user['lga']}")
        st.info(f"Community: {user['community']}")

        submitted = st.form_submit_button(
            "Submit Report",
            use_container_width=True
        )

    if submitted:

        if title.strip() == "" or description.strip() == "":

            st.error("Please complete all required fields.")
            return

        image_path = None

        if image:

            filename = f"{user['id']}_{image.name}"

            filepath = Path(UPLOAD_FOLDER) / filename

            with open(filepath, "wb") as f:
                f.write(image.getbuffer())

            image_path = str(filepath)

        create_report(

            user["id"],
            incident_type,
            severity,
            title,
            description,
            image_path,
            user["state"],
            user["lga"],
            user["community"]

        )

        st.success("✅ Report submitted successfully!")

        st.balloons()