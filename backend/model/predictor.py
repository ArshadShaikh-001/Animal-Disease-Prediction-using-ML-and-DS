import joblib
import pandas as pd
import os

# Get absolute path to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained artifacts safely
model = joblib.load(os.path.join(BASE_DIR, "disease_model.pkl"))
encoders = joblib.load(os.path.join(BASE_DIR, "encoders.pkl"))
target_encoder = joblib.load(os.path.join(BASE_DIR, "target_encoder.pkl"))


def predict_disease(animal_data, symptoms):
    input_data = {
        "Animal_Type": animal_data["animal_type"],
        "Age": float(animal_data["age"]),
        "Gender": animal_data["gender"],
        "Weight": float(animal_data["weight"]),

        "Appetite_Loss": 1 if "Loss of Appetite" in symptoms else 0,
        "Vomiting": 1 if "Vomiting" in symptoms else 0,
        "Diarrhea": 1 if "Diarrhea" in symptoms else 0,
        "Coughing": 1 if "Coughing" in symptoms else 0,
        "Labored_Breathing": 1 if "Labored Breathing" in symptoms else 0,
        "Lameness": 1 if "Lameness" in symptoms else 0,
        "Skin_Lesions": 1 if "Skin Lesions" in symptoms else 0,
        "Nasal_Discharge": 1 if "Nasal Discharge" in symptoms else 0,
        "Eye_Discharge": 1 if "Eye Discharge" in symptoms else 0,

        "Body_Temperature": 39.5,
        "Heart_Rate": 100
    }

    df = pd.DataFrame([input_data])

    # Encode categorical fields
    df["Animal_Type"] = encoders["Animal_Type"].transform(df["Animal_Type"])
    df["Gender"] = encoders["Gender"].transform(df["Gender"])

    pred_class = model.predict(df)[0]
    confidence = model.predict_proba(df).max()

    disease = target_encoder.inverse_transform([pred_class])[0]

    risk = "High" if confidence >= 0.75 else "Medium" if confidence >= 0.5 else "Low"

    return {
        "disease": disease,
        "confidence": round(confidence, 2),
        "risk": risk
    }
