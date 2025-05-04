# train.py

import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score, mean_squared_error
from xgboost import XGBRegressor
from preprocess import load_and_preprocess
from explainer import generate_global_shap_summary

# Load & preprocess
X, y = load_and_preprocess("Synthetic_Data_For_Students (2).csv")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=X['Injury Description'], random_state=42
)

# Columns
numerical_cols = X.select_dtypes(include=['float64', 'int64']).columns.tolist()
categorical_cols = ['Injury Description']

# Pipelines
numerical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])
categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
preprocessor = ColumnTransformer([
    ('num', numerical_pipeline, numerical_cols),
    ('cat', categorical_pipeline, categorical_cols)
])

# Transform
X_train_pre = preprocessor.fit_transform(X_train)
X_test_pre = preprocessor.transform(X_test)

# Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
train_clusters = kmeans.fit_predict(X_train_pre)
test_clusters = kmeans.predict(X_test_pre)

X_train_clustered = np.hstack((X_train_pre, train_clusters.reshape(-1, 1)))
X_test_clustered = np.hstack((X_test_pre, test_clusters.reshape(-1, 1)))

# Models
models = {
    'LinearRegression': LinearRegression(),
    'RandomForest': RandomForestRegressor(random_state=42),
    'XGBoost': XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42)
}

results = {}
best_r2 = -np.inf
best_model_name = None

for name, model in models.items():
    model.fit(X_train_clustered, y_train)
    y_train_pred = model.predict(X_train_clustered)
    y_test_pred = model.predict(X_test_clustered)

    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

    print(f"\n=== {name} with Clustering ===")
    print(f"Train R²: {train_r2:.4f}")
    print(f"Test R²:  {test_r2:.4f}")
    print(f"Test RMSE: {test_rmse:.2f}")

    if test_r2 > best_r2:
        best_r2 = test_r2
        best_model_name = name

    results[name] = {
        'model': model,
        'test_predictions': y_test_pred
    }

# Save best model
best_model = results[best_model_name]['model']
joblib.dump(best_model, f"best_model_{best_model_name.lower()}.joblib")
joblib.dump(preprocessor, "preprocessor.joblib")
joblib.dump(kmeans, "kmeans_cluster.joblib")
print(f"\n✅ Best model: {best_model_name}")

# Save predictions
output_df = X_test.copy()
output_df['Actual_SettlementValue'] = y_test.values
output_df['Predicted_SettlementValue'] = results[best_model_name]['test_predictions']
output_df.to_csv(f"{best_model_name.lower()}_predictions.csv", index=False)


generate_global_shap_summary(
    model_path="best_model_xgboost.joblib",
    preprocessor_path="preprocessor.joblib",
    kmeans_path="kmeans_cluster.joblib",
    original_data_path="Synthetic_Data_For_Students (2).csv",
    output_name="shap_summary.png"
)
