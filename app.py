import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

from src.predict import predict_yield
from src.irrigation import irrigation_advice


# --------------------------------------------------
# Page config
# --------------------------------------------------

st.set_page_config(
    page_title="Agricultural Intelligence",
    page_icon="🌾",
    layout="wide"
)


# --------------------------------------------------
# Load data/model
# --------------------------------------------------

model = joblib.load(
    "models/best_model.pkl"
)

features = joblib.load(
    "models/features.pkl"
)

data = pd.read_csv(
    "data/training_data.csv"
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title(
    "🌾 Agricultural Intelligence"
)

page = st.sidebar.radio(

    "Navigation",

    [
        "Home",
        "Yield Prediction",
        "Irrigation Advisor",
        "Weather vs Yield",
        "Regional Analytics"
    ]
)


# ==================================================
# HOME
# ==================================================

if page == "Home":

    st.title(
        "🌾 Agricultural Intelligence System"
    )

    st.subheader(
        "Crop Yield Prediction & Smart Irrigation Advisory"
    )

    st.write(
        """
        This system combines historical crop production,
        weather and soil information to provide:
       
        - Crop yield predictions
        - Weather-yield analysis
        - Water stress detection
        - Irrigation recommendations
        - Regional agricultural analytics
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Crop Records",
            len(data)
        )

    with col2:

        st.metric(
            "Districts",
            data["District"].nunique()
        )

    with col3:

        st.metric(
            "Crops",
            data["Crop"].nunique()
        )


# ==================================================
# YIELD PREDICTION
# ==================================================

elif page == "Yield Prediction":

    st.title(
        "🌾 Crop Yield Prediction"
    )

    col1, col2 = st.columns(2)

    with col1:

        crop = st.selectbox(
            "Crop",
            sorted(
                data["Crop"]
                .dropna()
                .unique()
            )
        )

        district = st.selectbox(
            "District",
            sorted(
                data["District"]
                .dropna()
                .unique()
            )
        )

        season = st.selectbox(
            "Season",
            sorted(
                data["Season"]
                .dropna()
                .unique()
            )
        )

        rainfall = st.number_input(
            "Seasonal Rainfall (mm)",
            min_value=0.0,
            value=1200.0
        )

        temperature = st.number_input(
            "Average Temperature (°C)",
            value=27.0
        )

    with col2:

        humidity = st.number_input(
            "Average Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=75.0
        )

        nitrogen = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            value=80.0
        )

        phosphorus = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            value=40.0
        )

        potassium = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            value=40.0
        )

        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5
        )

    if st.button(
        "🚀 Predict Yield",
        type="primary"
    ):

        prediction = predict_yield(

            crop=crop,

            district=district,

            season=season,

            rainfall=rainfall,

            avg_temperature=temperature,

            avg_humidity=humidity,

            nitrogen=nitrogen,

            phosphorus=phosphorus,

            potassium=potassium,

            ph=ph
        )

        st.success(
            "Prediction generated!"
        )

        st.metric(
            "Predicted Yield",
            f"{prediction:.2f} tons/hectare"
        )

        st.info(
            """
            This is a machine-learning estimate.
            Actual yield depends on field conditions,
            crop management, pests, diseases and other
            factors not represented in the model.
            """
        )


# ==================================================
# IRRIGATION
# ==================================================

elif page == "Irrigation Advisor":

    st.title(
        "💧 Smart Irrigation Advisor"
    )

    crop = st.selectbox(
        "Crop",
        sorted(
            data["Crop"]
            .dropna()
            .unique()
        )
    )

    temperature = st.number_input(
        "Today's Temperature (°C)",
        value=35.0
    )

    humidity = st.number_input(
        "Today's Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=45.0
    )

    rainfall_forecast = st.number_input(
        "Forecast Rainfall (mm)",
        min_value=0.0,
        value=0.0
    )

    recent_rainfall = st.number_input(
        "Rainfall in Last 24 Hours (mm)",
        min_value=0.0,
        value=0.0
    )

    if st.button(
        "💧 Check Water Stress",
        type="primary"
    ):

        result = irrigation_advice(

            temperature=temperature,

            humidity=humidity,

            rainfall_forecast=
                rainfall_forecast,

            recent_rainfall=
                recent_rainfall,

            crop=crop
        )

        level = result[
            "stress_level"
        ]

        irrigation = result[
            "irrigation_mm"
        ]

        if level == "HIGH":

            st.error(
                f"🔴 Water Stress: {level}"
            )

        elif level == "MODERATE":

            st.warning(
                f"🟡 Water Stress: {level}"
            )

        elif level == "LOW":

            st.info(
                f"🟢 Water Stress: {level}"
            )

        else:

            st.success(
                f"🟢 Water Stress: {level}"
            )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Stress Score",
                result["stress_score"]
            )

        with col2:

            st.metric(
                "Suggested Irrigation",
                f"{irrigation} mm"
            )

        st.write(
            result["message"]
        )


# ==================================================
# WEATHER VS YIELD
# ==================================================

elif page == "Weather vs Yield":

    st.title(
        "🌦️ Weather-Yield Correlation Explorer"
    )

    crop = st.selectbox(
        "Select Crop",
        sorted(
            data["Crop"]
            .dropna()
            .unique()
        )
    )

    variable = st.selectbox(
        "Weather Variable",
        [
            "Rainfall",
            "AvgTemperature",
            "AvgHumidity"
        ]
    )

    filtered = data[
        data["Crop"] == crop
    ]

    fig = px.scatter(

        filtered,

        x=variable,

        y="Yield",

        trendline="ols",

        hover_data=[
            "District",
            "Year"
        ],

        title=(
            f"{variable} vs Yield - "
            f"{crop}"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==================================================
# REGIONAL ANALYTICS
# ==================================================

elif page == "Regional Analytics":

    st.title(
        "🗺️ Regional Production Analytics"
    )

    crop = st.selectbox(
        "Select Crop",
        sorted(
            data["Crop"]
            .dropna()
            .unique()
        )
    )

    filtered = data[
        data["Crop"] == crop
    ]

    district_data = (
        filtered
        .groupby("District")
        ["Yield"]
        .mean()
        .reset_index()
    )

    district_data = district_data.sort_values(
        "Yield",
        ascending=False
    )

    st.subheader(
        "Average Yield by District"
    )

    fig = px.bar(

        district_data.head(20),

        x="Yield",

        y="District",

        orientation="h",

        color="Yield",

        color_continuous_scale="RdYlGn"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Top Performing Districts"
    )

    st.dataframe(
        district_data.head(10),
        use_container_width=True
    )

