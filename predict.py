import joblib
import pandas as pd


model = joblib.load(
    "models/best_model.pkl"
)

features = joblib.load(
    "models/features.pkl"
)


def predict_yield(
    crop,
    district,
    season,
    rainfall,
    avg_temperature,
    avg_humidity,
    nitrogen,
    phosphorus,
    potassium,
    ph
):

    data = pd.DataFrame([{

        "Crop": crop,

        "District": district,

        "Season": season,

        "Rainfall": rainfall,

        "AvgTemperature":
            avg_temperature,

        "AvgHumidity":
            avg_humidity,

        "N": nitrogen,

        "P": phosphorus,

        "K": potassium,

        "pH": ph
    }])

    data = data[features]

    prediction = model.predict(
        data
    )[0]

    return prediction


if __name__ == "__main__":

    prediction = predict_yield(

        crop="Rice",

        district="Thrissur",

        season="Kharif",

        rainfall=1500,

        avg_temperature=27,

        avg_humidity=78,

        nitrogen=90,

        phosphorus=40,

        potassium=45,

        ph=6.5
    )

    print(
        f"Predicted yield: "
        f"{prediction:.2f} tons/hectare"
    )

