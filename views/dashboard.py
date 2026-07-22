import streamlit as st
import plotly.express as px
import pandas as pd

from database.reports import (
    report_statistics,
    get_latest_reports,
    reports_by_severity,
    reports_by_type,
    reports_last_24h
)
from services.risk_engine import calculate_risk

from services.trust_engine import get_badge
from services.advisory_engine import generate_advisory
from services.weather import get_weather


def show_dashboard(user):

    with st.spinner("Loading community reports..."):
        stats = report_statistics()

    risk = calculate_risk(
        stats["total_reports"],
        stats["critical_reports"]
    )

    with st.spinner("Fetching latest weather..."):
        weather = get_weather(user["state"])

    advisory = generate_advisory(
        risk,
        weather,
        language=user.get("language", "English")
    )

    st.title("🌍 ClimateGuardian AI")

    st.subheader(f"Welcome back, {user['full_name']} 👋")

    st.write(
        "Monitor climate risks, environmental hazards and community reports in real time."
    )

    st.divider()

    tab_overview, tab_community, tab_profile, tab_analytics = st.tabs(
        ["🛰 Overview", "📢 Community", "👤 Profile", "📊 Analytics"]
    )

    # =====================================
    # TAB: OVERVIEW
    # =====================================

    with tab_overview:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🚨 Total Reports",
                stats["total_reports"]
            )

        with col2:
            st.metric(
                "🔴 Critical Reports",
                stats["critical_reports"]
            )

        with col3:
            st.metric(
                "🛰 Community Risk",
                risk["status"]
            )

        with col4:
            if weather:
                st.metric(
                    "🌡 Temperature",
                    f"{weather['temperature']}°C"
                )
            else:
                st.metric(
                    "🌡 Temperature",
                    "--"
                )

        st.divider()

        st.subheader("🛰 Live Community Risk Monitor")

        recent_count = reports_last_24h()

        st.caption(
            f"⏱ {recent_count} community report(s) in the last 24 hours "
            "feeding this early-warning score in real time."
        )

        progress = min(risk["score"], 100)

        st.progress(progress)

        st.write(f"### Risk Score: **{risk['score']}/100**")

        if risk["score"] < 20:
            st.success("Community currently has a LOW climate risk.")

        elif risk["score"] < 50:
            st.warning("Community should remain alert.")

        elif risk["score"] < 80:
            st.warning("High climate risk detected.")

        else:
            st.error("Critical community risk detected.")

        st.divider()

        st.subheader("🌤 Current Weather")

        if weather:

            with st.container(border=True):

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "🌡 Temperature",
                    f"{weather['temperature']}°C"
                )

                c2.metric(
                    "💧 Humidity",
                    f"{weather['humidity']}%"
                )

                c3.metric(
                    "💨 Wind",
                    f"{weather['wind']} km/h"
                )

        else:

            st.info("Weather service unavailable.")

    # =====================================
    # TAB: COMMUNITY
    # =====================================

    with tab_community:

        st.subheader("📢 Government Safety Advisory")

        st.success(
            f"{advisory['icon']} Risk Level: {advisory['level']}"
        )

        st.write(advisory["message"])

        st.divider()

        st.subheader("📢 Community Situation")

        if stats["total_reports"] == 0:

            st.success(
                "No incidents have been reported in your community."
            )

        else:

            st.warning(
                f"{stats['total_reports']} incident(s) have been reported."
            )

            if stats["critical_reports"] > 0:

                st.error(
                    f"{stats['critical_reports']} report(s) are CRITICAL."
                )

        st.divider()

        st.subheader("📰 Community Intelligence")

        with st.spinner("Loading latest community reports..."):
            reports = get_latest_reports()

        if len(reports) == 0:

            st.info(
                "No community reports have been submitted yet."
            )

        else:

            for report in reports:

                with st.container(border=True):

                    st.markdown(f"### 🚨 {report['title']}")

                    st.caption(
                        f"{report['incident_type']} • {report['created_at']}"
                    )

                    st.write(
                        f"**Incident:** {report['incident_type']}"
                    )

                    st.write(
                        f"📍 {report['community']}, {report['lga']}"
                    )

                    st.caption(
                        f"👤 Reported by {report['full_name']}"
                    )

                    st.write(report["description"])
                    if report["image_path"]:
                        st.image(
                            report["image_path"],
                            use_container_width=True
                        )

                    severity = report["severity"]

                    if severity == "Critical":
                        st.error("🔴 Critical")
                    elif severity == "High":
                        st.warning("🟠 High")
                    elif severity == "Moderate":
                        st.info("🟡 Moderate")
                    else:
                        st.success("🟢 Low")

    # =====================================
    # TAB: PROFILE
    # =====================================

    with tab_profile:

        st.subheader("👤 My Profile")

        trust = user.get("trust_score", 50)

        # derive and show trust badge
        badge = get_badge(trust)
        st.success(badge)

        st.progress(trust / 100)

        st.metric(
            "🏅 Trust Score",
            f"{trust}/100"
        )

        if trust >= 90:
            st.success("Elite Reporter")
        elif trust >= 70:
            st.success("Trusted Member")
        elif trust >= 40:
            st.info("Community Member")
        else:
            st.warning("New Member")

        st.write(f"**Name:** {user['full_name']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Role:** {user['user_type']}")
        st.write(f"**State:** {user['state']}")
        st.write(f"**LGA:** {user['lga']}")
        st.write(f"**Community:** {user['community']}")

        st.divider()

        st.subheader("🤖 Gemma AI")

        with st.spinner("Checking Gemma status..."):
            st.warning("Offline")

        st.caption(
            "Gemma will run locally on this computer during the hackathon."
        )

        st.divider()

        st.subheader("📊 Community Health")

        st.metric(
            "Community Status",
            risk["status"]
        )

    # =====================================
    # TAB: ANALYTICS
    # =====================================

    with tab_analytics:

        st.header("📊 Incident Analytics")

        with st.spinner("Loading analytics..."):
            severity_data = reports_by_severity()
            type_data = reports_by_type()

        chart_left, chart_right = st.columns(2)

        with chart_left:

            st.subheader("Reports by Severity")

            if severity_data:

                df = pd.DataFrame(
                    severity_data,
                    columns=["Severity", "Reports"]
                )

                fig = px.bar(
                    df,
                    x="Severity",
                    y="Reports",
                    text="Reports",
                    color="Severity"
                )

                fig.update_layout(
                    height=350,
                    showlegend=False
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info("No reports yet.")

        with chart_right:

            st.subheader("Incident Categories")

            if type_data:

                df = pd.DataFrame(
                    type_data,
                    columns=["Incident", "Reports"]
                )

                fig = px.pie(
                    df,
                    names="Incident",
                    values="Reports",
                    hole=0.45
                )

                fig.update_layout(height=350)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info("No reports yet.")