from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import os

# Initialize FastAPI
app = FastAPI()

# Load pre-trained models and transformers
MODEL_DIR = os.path.join("models")
preprocessor = joblib.load(os.path.join(MODEL_DIR, "preprocessor.joblib"))
kmeans = joblib.load(os.path.join(MODEL_DIR, "kmeans_cluster.joblib"))
model = joblib.load(os.path.join(MODEL_DIR, "best_model_xgboost.joblib"))

# ✅ Step 1: Define Pydantic input with clean field names
class ClaimInput(BaseModel):
    accident_type: str
    injury_prognosis: str
    special_health_expenses: float = 0.0
    special_reduction: float = 0.0
    special_overage: float = 0.0
    general_rest: float = 0.0
    special_additional_injury: float = 0.0
    special_earnings_loss: float = 0.0
    special_usage_loss: float = 0.0
    special_medications: float = 0.0
    special_asset_damage: float = 0.0
    special_rehabilitation: float = 0.0
    special_fixes: float = 0.0
    general_fixed: float = 0.0
    general_uplift: float = 0.0
    special_loaner_vehicle: float = 0.0
    special_trip_costs: float = 0.0
    special_journey_expenses: float = 0.0
    special_therapy: float = 0.0
    exceptional_circumstances: str
    minor_psychological_injury: str
    dominant_injury: str
    whiplash: str
    vehicle_type: str
    weather_conditions: str
    vehicle_age: int = 0
    driver_age: int = 0
    number_of_passengers: int = 0
    accident_description: str
    injury_description: str
    police_report_filed: str
    witness_present: str
    gender: str

# ✅ Step 2: Prediction endpoint
@app.post("/predict/")
def predict_settlement(input: ClaimInput):
    data = input.model_dump()  # Pydantic v2 compatible
    df = pd.DataFrame([data])

    # ✅ Step 3: Rename to match training feature names
    rename_map = {
        'accident_type': 'AccidentType',  # ✅ Updated to match model
        'injury_prognosis': 'Injury_Prognosis',
        'special_health_expenses': 'SpecialHealthExpenses',
        'special_reduction': 'SpecialReduction',
        'special_overage': 'SpecialOverage',
        'general_rest': 'GeneralRest',
        'special_additional_injury': 'SpecialAdditionalInjury',
        'special_earnings_loss': 'SpecialEarningsLoss',
        'special_usage_loss': 'SpecialUsageLoss',
        'special_medications': 'SpecialMedications',
        'special_asset_damage': 'SpecialAssetDamage',
        'special_rehabilitation': 'SpecialRehabilitation',
        'special_fixes': 'SpecialFixes',
        'general_fixed': 'GeneralFixed',
        'general_uplift': 'GeneralUplift',
        'special_loaner_vehicle': 'SpecialLoanerVehicle',
        'special_trip_costs': 'SpecialTripCosts',
        'special_journey_expenses': 'SpecialJourneyExpenses',
        'special_therapy': 'SpecialTherapy',
        'exceptional_circumstances': 'Exceptional_Circumstances',
        'minor_psychological_injury': 'Minor_Psychological_Injury',
        'dominant_injury': 'Dominant injury',
        'whiplash': 'Whiplash',
        'vehicle_type': 'Vehicle Type',
        'weather_conditions': 'Weather Conditions',
        'vehicle_age': 'Vehicle Age',
        'driver_age': 'Driver Age',
        'number_of_passengers': 'Number of Passengers',
        'accident_description': 'Accident Description',
        'injury_description': 'Injury Description',
        'police_report_filed': 'Police Report Filed',
        'witness_present': 'Witness Present',
        'gender': 'Gender'
    }

    df = df.rename(columns=rename_map)

    # ✅ Step 4: Feature Engineering
    df['Exceptional_Circumstances'] = df['Exceptional_Circumstances'].map({'Yes': 1, 'No': 0})
    df['Minor_Psychological_Injury'] = df['Minor_Psychological_Injury'].map({'Yes': 1, 'No': 0})
    df['Whiplash'] = df['Whiplash'].map({'Yes': 1, 'No': 0})
    df['Police Report Filed'] = df['Police Report Filed'].map({'Yes': 1, 'No': 0})
    df['Witness Present'] = df['Witness Present'].map({'Yes': 1, 'No': 0})
    df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})

    df['prognosis_weeks'] = df['Injury_Prognosis'].str.extract(r'(\d+)').astype(float).fillna(0)
    df['Description_Length'] = df['Accident Description'].apply(lambda x: len(str(x).split()))
    df['Injury Description'] = df['Injury Description'].fillna("Missing")

    # ✅ Step 5: Add placeholder column expected by preprocessor
    df['Days_To_Claim'] = 0  # if not available, default to 0

    # ✅ Step 6: Use full feature set
    X_input = df.copy()

    # Optional sanity check
    required_columns = getattr(preprocessor, "feature_names_in_", [])
    missing = set(required_columns) - set(X_input.columns)
    if missing:
        raise ValueError(f"❌ Missing columns for preprocessing: {missing}")

    # ✅ Step 7: Preprocess, Cluster, Predict
    X_transformed = preprocessor.transform(X_input)
    cluster = kmeans.predict(X_transformed)[0]
    X_final = np.hstack((X_transformed, [[cluster]]))
    prediction = model.predict(X_final)[0]

    return {
        "predicted_settlement": round(float(prediction), 2),
        "cluster": int(cluster)
    }
