
# train_core_model.py
import pandas as pd
import numpy as np
import joblib
import shap
import lime.lime_tabular

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Load data
data = pd.read_csv('./dataset/sample_claims.csv')

# Feature Engineering
data['gender'] = data['gender'].map({'Male': 0, 'Female': 1})
data['prognosis_weeks'] = data['prognosis'].str.extract(r'(\d+)').astype(float)

# Select features
features = ['age', 'gender', 'income', 'prognosis_weeks']
X = data[features]
y = data['claim_amount']
groups = data['injury_type']

# Split data
X_train, X_test, y_train, y_test, groups_train, groups_test = train_test_split(
    X, y, groups, test_size=0.2, random_state=42
)

# Level 1 Model: Classifier
group_classifier = DecisionTreeClassifier(max_depth=5, random_state=42)
group_classifier.fit(X_train, groups_train)

# Train separate models for each injury type
group_models = {}
unique_groups = groups_train.unique()

for group in unique_groups:
    idx = groups_train == group
    X_group = X_train[idx]
    y_group = y_train[idx]

    # Choose model type based on group
    if group in ['Whiplash', 'Back Injury']:
        model = LinearRegression()
    else:
        model = DecisionTreeRegressor(max_depth=5, random_state=42)

    model.fit(X_group, y_group)
    group_models[group] = model

# Save models
joblib.dump(group_classifier, './core_model/group_classifier.pkl')
for group, model in group_models.items():
    joblib.dump(model, f'./core_model/model_{group.replace(" ", "_")}.pkl')

print("Models saved!")

# Example Explainability with SHAP
explainer = shap.TreeExplainer(group_classifier)
shap_values = explainer.shap_values(X_test)
print("SHAP values for group classifier generated!")

# Optional: Example Explainability with LIME
lime_explainer = lime.lime_tabular.LimeTabularExplainer(
    X_train.values, feature_names=features, class_names=unique_groups, verbose=True, mode='classification'
)

print("LIME explainer for group classifier ready!")
