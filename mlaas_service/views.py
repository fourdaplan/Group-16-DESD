# mlaas_service/views.py

import pandas as pd
from joblib import load
from django.http import JsonResponse
from rest_framework.decorators import api_view

scaler = load("mlaas_service/models/core_model/scaler.joblib")
classifier = load("mlaas_service/models/core_model/group_classifier.joblib")

@api_view(['POST'])
def predict_settlement(request):
    data = request.data
    df = pd.DataFrame([data])

    X_scaled = scaler.transform(df)
    group = classifier.predict(X_scaled)[0]

    model = load(f"mlaas_service/models/core_model/group_{group}_regressor.joblib")
    prediction = model.predict(X_scaled)[0]

    return JsonResponse({
        "predicted_settlement_gbp": round(prediction, 2),
        "group": int(group)
    })
