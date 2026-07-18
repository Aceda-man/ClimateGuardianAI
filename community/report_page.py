import streamlit as st

from community.reports import add_report



def report_page(user):


    st.header(
        "📢 Report Climate Incident"
    )


    st.write(
        f"""
        Location:

        {user['community']},
        {user['lga']},
        {user['state']}
        """
    )


    category = st.selectbox(

        "Incident Category",

        [

        "Flood",

        "Drought",

        "Extreme Heat",

        "Crop Damage",

        "Livestock Loss",

        "Fishery Problem",

        "Property Damage",

        "Other"

        ]

    )


    issue = st.text_input(
        "Describe the problem"
    )


    description = st.text_area(
        "Additional Information"
    )


    image = st.file_uploader(
        "Upload Image (Optional)",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )


    image_name = None


    if image:

        image_name = image.name


        st.image(
            image,
            width=300
        )


    if st.button(
        "Submit Report"
    ):


        add_report(

            user,

            category,

            issue,

            description,

            image_name

        )


        st.success(
            "Report submitted successfully."
        )