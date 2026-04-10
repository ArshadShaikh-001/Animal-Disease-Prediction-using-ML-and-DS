import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# 1. LOAD DATA
# -----------------------------
df = pd.read_csv("../data/animal_disease.csv")

# Normalize column names (safety)
df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace(".", "_")
)

# -----------------------------
# 2. CLEAN & PREPROCESS
# -----------------------------

# Convert Yes/No columns to 1/0
binary_cols = [
    "Appetite_Loss",
    "Vomiting",
    "Diarrhea",
    "Coughing",
    "Labored_Breathing",
    "Lameness",
    "Skin_Lesions",
    "Nasal_Discharge",
    "Eye_Discharge"
]

for col in binary_cols:
    df[col] = df[col].map({"Yes": 1, "No": 0})

# Clean temperature column (remove °C / Â°C)
df["Body_Temperature"] = (
    df["Body_Temperature"]
    .astype(str)
    .str.replace("Â°C", "")
    .str.replace("°C", "")
    .astype(float)
)

# -----------------------------
# 3. ENCODE CATEGORICAL DATA
# -----------------------------
label_encoders = {}

for col in ["Animal_Type", "Gender"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Target encoder
target_encoder = LabelEncoder()
df["Disease_Prediction"] = target_encoder.fit_transform(df["Disease_Prediction"])

# -----------------------------
# 4. SELECT FEATURES & TARGET
# -----------------------------
feature_cols = [
    "Animal_Type",
    "Age",
    "Gender",
    "Weight",
    "Appetite_Loss",
    "Vomiting",
    "Diarrhea",
    "Coughing",
    "Labored_Breathing",
    "Lameness",
    "Skin_Lesions",
    "Nasal_Discharge",
    "Eye_Discharge",
    "Body_Temperature",
    "Heart_Rate"
]

X = df[feature_cols]
y = df["Disease_Prediction"]

# -----------------------------
# 5. TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# 6. TRAIN MODEL
# -----------------------------
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# -----------------------------
# 7. SAVE MODEL & ENCODERS
# -----------------------------
os.makedirs(".", exist_ok=True)

joblib.dump(model, "disease_model.pkl")
joblib.dump(label_encoders, "encoders.pkl")
joblib.dump(target_encoder, "target_encoder.pkl")

print("✅ Model trained and saved successfully")

# Developed By Team AV 
# 1. Arshad Shaikh
# 2. Atharva Wadekar
# 3. Kartikey Dhale