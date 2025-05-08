from django.conf import settings
from joblib import load
import pandas as pd
import numpy as np
from django.http import JsonResponse
from rest_framework.decorators import api_view
import os

MODEL_DIR = os.path.join(settings.MEDIA_ROOT, "ai_models")

preprocessor = load(os.path.join(MODEL_DIR, "preprocessor.joblib"))
kmeans = load(os.path.join(MODEL_DIR, "kmeans_cluster.joblib"))
model = load(os.path.join(MODEL_DIR, "best_model_xgboost.joblib"))

@api_view(["POST"])
def predict_settlement(request):
    print("🔍 Received prediction request:", request.data)

    # Convert request to DataFrame
    raw_data = dict(request.data)
    df = pd.DataFrame([raw_data])

    # Rename fields to match trained feature names
    rename_map = {
        'accident_type': 'AccidentType',  # ✅ Fixed (was 'Accident Type')
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

    # Type casting
    float_fields = [
        'SpecialHealthExpenses', 'SpecialReduction', 'SpecialOverage', 'GeneralRest',
        'SpecialAdditionalInjury', 'SpecialEarningsLoss', 'SpecialUsageLoss',
        'SpecialMedications', 'SpecialAssetDamage', 'SpecialRehabilitation', 'SpecialFixes',
        'GeneralFixed', 'GeneralUplift', 'SpecialLoanerVehicle', 'SpecialTripCosts',
        'SpecialJourneyExpenses', 'SpecialTherapy'
    ]
    int_fields = ['Vehicle Age', 'Driver Age', 'Number of Passengers']

    for field in float_fields:
        df[field] = df[field].astype(float)
    for field in int_fields:
        df[field] = df[field].astype(int)

    # Binary encoding
    df['Exceptional_Circumstances'] = df['Exceptional_Circumstances'].map({'Yes': 1, 'No': 0})
    df['Minor_Psychological_Injury'] = df['Minor_Psychological_Injury'].map({'Yes': 1, 'No': 0})
    df['Whiplash'] = df['Whiplash'].map({'Yes': 1, 'No': 0})
    df['Police Report Filed'] = df['Police Report Filed'].map({'Yes': 1, 'No': 0})
    df['Witness Present'] = df['Witness Present'].map({'Yes': 1, 'No': 0})
    df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})

    # Feature engineering
    df['prognosis_weeks'] = df['Injury_Prognosis'].str.extract(r'(\d+)').astype(float).fillna(0)
    df['Description_Length'] = df['Accident Description'].apply(lambda x: len(str(x).split()))
    df['Injury Description'] = df['Injury Description'].fillna("Missing")

    # ✅ Add missing column required by model
    df['Days_To_Claim'] = 0

    # ✅ Use full feature set (don't limit to 6 columns)
    X_input = df.copy()

    # ✅ Optional check for missing features
    required_columns = getattr(preprocessor, "feature_names_in_", [])
    missing = set(required_columns) - set(X_input.columns)
    if missing:
        return JsonResponse({"error": f"Missing columns: {missing}"}, status=400)

    # Predict
    X_transformed = preprocessor.transform(X_input)
    cluster = kmeans.predict(X_transformed)[0]
    prediction = model.predict(np.hstack((X_transformed, [[cluster]])))[0]

    return JsonResponse({
        "predicted_settlement_gbp": round(float(prediction), 2),
        "cluster": int(cluster)
    })
