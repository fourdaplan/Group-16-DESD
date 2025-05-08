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

# Define expected input structure
class ClaimInput(BaseModel):
    Accident_Type: str
    Injury_Prognosis: str
    SpecialHealthExpenses: float = 0.0
    SpecialReduction: float = 0.0
    SpecialOverage: float = 0.0
    GeneralRest: float = 0.0
    SpecialAdditionalInjury: float = 0.0
    SpecialEarningsLoss: float = 0.0
    SpecialUsageLoss: float = 0.0
    SpecialMedications: float = 0.0
    SpecialAssetDamage: float = 0.0
    SpecialRehabilitation: float = 0.0
    SpecialFixes: float = 0.0
    GeneralFixed: float = 0.0
    GeneralUplift: float = 0.0
    SpecialLoanerVehicle: float = 0.0
    SpecialTripCosts: float = 0.0
    SpecialJourneyExpenses: float = 0.0
    SpecialTherapy: float = 0.0
    Exceptional_Circumstances: str
    Minor_Psychological_Injury: str
    Dominant_injury: str
    Whiplash: str
    Vehicle_Type: str
    Weather_Conditions: str
    Vehicle_Age: int = 0
    Driver_Age: int = 0
    Number_of_Passengers: int = 0
    Accident_Description: str
    Injury_Description: str
    Police_Report_Filed: str
    Witness_Present: str
    Gender: str

@app.post("/predict/")
def predict_settlement(input: ClaimInput):
    # Convert input to DataFrame
    data = input.dict()
    df = pd.DataFrame([data])

    # Feature Engineering
    df['Exceptional_Circumstances'] = df['Exceptional_Circumstances'].map({'Yes': 1, 'No': 0})
    df['Minor_Psychological_Injury'] = df['Minor_Psychological_Injury'].map({'Yes': 1, 'No': 0})
    df['Whiplash'] = df['Whiplash'].map({'Yes': 1, 'No': 0})
    df['Police_Report_Filed'] = df['Police_Report_Filed'].map({'Yes': 1, 'No': 0})
    df['Witness_Present'] = df['Witness_Present'].map({'Yes': 1, 'No': 0})
    df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})

    # Injury Prognosis weeks extraction
    df['prognosis_weeks'] = df['Injury_Prognosis'].str.extract(r'(\d+)').astype(float).fillna(0)

    # Description length
    df['Description_Length'] = df['Accident_Description'].apply(lambda x: len(str(x).split()))

    # Injury Description filling if empty
    df['Injury_Description'] = df['Injury_Description'].fillna("Missing")

    # Select relevant columns (same as training)
    features = [
        'Driver_Age', 'Gender', 'SpecialHealthExpenses', 'prognosis_weeks',
        'Injury_Description', 'Description_Length'
    ]

    X_input = df.rename(columns={
        'Driver_Age': 'age',
        'Gender': 'gender',
        'SpecialHealthExpenses': 'income',
        'prognosis_weeks': 'prognosis_weeks',
        'Injury_Description': 'Injury Description',
        'Description_Length': 'Description_Length'
    })

    X_input = X_input[['age', 'gender', 'income', 'prognosis_weeks', 'Injury Description', 'Description_Length']]

    # Preprocess input
    X_transformed = preprocessor.transform(X_input)

    # Cluster
    cluster = kmeans.predict(X_transformed)[0]

    # Add cluster to input
    X_final = np.hstack((X_transformed, [[cluster]]))

    # Predict
    prediction = model.predict(X_final)[0]

    return {
        "predicted_settlement": round(float(prediction), 2),
        "cluster": int(cluster)
    }
