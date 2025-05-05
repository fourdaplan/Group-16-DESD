import os
from django.conf import settings
from joblib import load
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view

MODEL_DIR = os.path.join(settings.MEDIA_ROOT, "ai_models")

preprocessor = load(os.path.join(MODEL_DIR, "preprocessor.joblib"))
kmeans = load(os.path.join(MODEL_DIR, "kmeans_cluster.joblib"))
model = load(os.path.join(MODEL_DIR, "best_model_xgboost.joblib"))

@api_view(["POST"])
def predict_settlement(request):
    print("🔍 Received prediction request:", request.data)  # Add this line

    data = request.data
    df = pd.DataFrame([data])
    
    df_transformed = preprocessor.transform(df)
    cluster = kmeans.predict(df_transformed)[0]
    prediction = model.predict(np.hstack((df_transformed, [[cluster]])))[0]

    return JsonResponse({
        "predicted_settlement_gbp": round(prediction, 2),
        "cluster": int(cluster)
    })
