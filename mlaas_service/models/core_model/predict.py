# predict.py

import pandas as pd
import numpy as np
import joblib

def make_prediction(new_data: pd.DataFrame):
    preprocessor = joblib.load("preprocessor.joblib")
    kmeans = joblib.load("kmeans_cluster.joblib")
    model = joblib.load("best_model_xgboost.joblib")  # or match saved model name

    # Preprocess input
    X_pre = preprocessor.transform(new_data)
    clusters = kmeans.predict(X_pre)
    X_final = np.hstack((X_pre, clusters.reshape(-1, 1)))

    # Predict
    predictions = model.predict(X_final)
    return predictions
