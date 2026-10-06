def calculate_water_stress(
    temperature,
    humidity,
    rainfall_forecast,
    recent_rainfall,
    crop
):

    stress_score = 0

    # Temperature stress
    if temperature >= 35:
        stress_score += 3

    elif temperature >= 30:
        stress_score += 2

    elif temperature >= 27:
        stress_score += 1

    # Humidity stress
    if humidity < 40:
        stress_score += 3

    elif humidity < 60:
        stress_score += 2

    elif humidity < 70:
        stress_score += 1

    # Rainfall
    if rainfall_forecast < 2:
        stress_score += 2

    elif rainfall_forecast < 5:
        stress_score += 1

    # Recent rain reduces stress
    if recent_rainfall >= 10:
        stress_score -= 3

    elif recent_rainfall >= 5:
        stress_score -= 2

    # Don't allow negative
    stress_score = max(
        stress_score,
        0
    )

    # Classification
    if stress_score >= 7:

        level = "HIGH"
        irrigation = 15

    elif stress_score >= 4:

        level = "MODERATE"
        irrigation = 10

    elif stress_score >= 2:

        level = "LOW"
        irrigation = 5

    else:

        level = "NONE"
        irrigation = 0

    return {
        "stress_score": stress_score,
        "stress_level": level,
        "irrigation_mm": irrigation
    }


def irrigation_advice(
    temperature,
    humidity,
    rainfall_forecast,
    recent_rainfall,
    crop
):

    result = calculate_water_stress(

        temperature,
        humidity,
        rainfall_forecast,
        recent_rainfall,
        crop
    )

    level = result["stress_level"]

    if level == "HIGH":

        message = (
            "High water stress. "
            "Irrigation is recommended."
        )

    elif level == "MODERATE":

        message = (
            "Moderate water stress. "
            "Monitor the field and consider irrigation."
        )

    elif level == "LOW":

        message = (
            "Low water stress. "
            "Small irrigation may be sufficient."
        )

    else:

        message = (
            "No significant water stress. "
            "Irrigation may not be required."
        )

    result["message"] = message

    return result

