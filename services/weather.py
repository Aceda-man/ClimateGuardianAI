import requests

# Coordinates of major Nigerian states
LOCATIONS = {
    "Kwara": (8.4966, 4.5421),
    "Lagos": (6.5244, 3.3792),
    "Abuja": (9.0765, 7.3986),
    "Oyo": (7.3775, 3.9470),
    "Kano": (12.0022, 8.5920),
    "Rivers": (4.8156, 7.0498),
    "Kaduna": (10.5105, 7.4165),
}


def get_weather(state):
    """
    Returns current weather for a Nigerian state.
    """

    if state not in LOCATIONS:
        state = "Kwara"

    lat, lon = LOCATIONS[state]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,"
        "wind_speed_10m,weather_code"
    )

    try:
        response = requests.get(url, timeout=5)
        data = response.json()["current"]

        return {
            "temperature": data["temperature_2m"],
            "humidity": data["relative_humidity_2m"],
            "wind": data["wind_speed_10m"],
            "code": data["weather_code"]
        }

    except Exception:
        return None