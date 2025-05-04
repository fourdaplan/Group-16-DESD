# explainer.py

import shap
import matplotlib.pyplot as plt
import os
import joblib
import pandas as pd
import numpy as np

def generate_global_shap_summary(model_path, preprocessor_path, kmeans_path, original_data_path, output_name="shap_summary.png"):
    # Load artifacts
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    kmeans = joblib.load(kmeans_path)

    # Load data again
    from preprocess import load_and_preprocess
    X, y = load_and_preprocess(original_data_path)

    # Re-transform data
    X_transformed = preprocessor.transform(X)
    clusters = kmeans.predict(X_transformed)
    X_clustered = np.hstack((X_transformed, clusters.reshape(-1, 1)))

    # Use SHAP KernelExplainer for most compatibility
    print("🔍 Generating SHAP values...")
    explainer = shap.Explainer(model.predict, X_clustered)
    shap_values = explainer(X_clustered[:100])  # Use a sample for speed

    # Save summary
    output_path = os.path.join(os.path.dirname(__file__), output_name)
    shap.summary_plot(shap_values, X_clustered[:100], show=False)
    plt.savefig(output_path)
    plt.close()
    print(f"✅ SHAP summary saved to: {output_path}")
