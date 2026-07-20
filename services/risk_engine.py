def calculate_risk(total_reports, critical_reports):

    score = 0

    score += total_reports * 3
    score += critical_reports * 12

    if score < 20:

        return {
            "status": "🟢 Safe",
            "score": score
        }

    elif score < 50:

        return {
            "status": "🟡 Moderate Risk",
            "score": score
        }

    elif score < 80:

        return {
            "status": "🟠 High Risk",
            "score": score
        }

    else:

        return {
            "status": "🔴 Critical",
            "score": score
        }