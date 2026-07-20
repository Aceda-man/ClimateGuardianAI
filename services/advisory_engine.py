def generate_advisory(risk, weather=None):

    score = risk["score"]

    if score >= 80:
        return {
            "icon": "🔴",
            "level": "Critical",
            "message":
                "Multiple high-risk incidents have been reported. Residents should avoid affected areas and follow instructions from local authorities."
        }

    elif score >= 50:
        return {
            "icon": "🟠",
            "level": "High",
            "message":
                "Community members should remain vigilant and report any new incidents immediately."
        }

    elif score >= 20:
        return {
            "icon": "🟡",
            "level": "Moderate",
            "message":
                "Conditions are stable but require monitoring. Continue reporting environmental hazards."
        }

    else:
        return {
            "icon": "🟢",
            "level": "Low",
            "message":
                "No significant threats detected. Continue monitoring your surroundings."
        }