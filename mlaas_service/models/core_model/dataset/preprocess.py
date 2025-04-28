# full_preprocessing_and_clustering.py

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans

# Step 1: Load the dataset
file_path = 'Synthetic_Data_For_Students (2).csv'  # Change this if your file is in another location

df_full = pd.read_csv(file_path)

# Step 2: Process Dates
# Convert Accident Date and Claim Date to datetime
# and create Days_To_Claim

# Parsing dates carefully
df_full['Accident Date'] = pd.to_datetime(df_full['Accident Date'], errors='coerce', format='%d/%m/%Y')
df_full['Claim Date'] = pd.to_datetime(df_full['Claim Date'], errors='coerce', format='%d/%m/%Y')

# Calculate Days_To_Claim
df_full['Days_To_Claim'] = (df_full['Claim Date'] - df_full['Accident Date']).dt.days

# Drop raw date columns
df_full = df_full.drop(columns=['Accident Date', 'Claim Date'])

# Step 3: Process Boolean Fields (Yes/No to 1/0)
bool_cols = ['Police Report Filed', 'Witness Present', 'Whiplash', 'Exceptional_Circumstances', 'Minor_Psychological_Injury']
for col in bool_cols:
    if col in df_full.columns:
        df_full[col] = df_full[col].map({'Yes': 1, 'No': 0})

# Step 4: Handle Missing Text Fields
text_cols = ['Accident Description', 'Injury Description']
for col in text_cols:
    if col in df_full.columns:
        df_full[col] = df_full[col].fillna('Missing')

# Step 5: Separate Features and Target
target_col = 'SettlementValue'
X = df_full.drop(columns=[target_col])
y = df_full[target_col]

# Step 6: Identify Numerical and Categorical Columns
numerical_cols = X.select_dtypes(include=['float64', 'int64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

# Step 7: Define Label Encoding Function
def label_encode_dataframe(X_cat):
    X_cat = pd.DataFrame(X_cat)
    encoded = pd.DataFrame()
    for col in X_cat.columns:
        le = LabelEncoder()
        X_cat[col] = X_cat[col].fillna('Missing')
        encoded[col] = le.fit_transform(X_cat[col])
    return encoded.values

# Step 8: Define Pipelines
numerical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('label_encoder', FunctionTransformer(label_encode_dataframe, validate=False))
])

# Step 9: Combine Pipelines into Preprocessor
preprocessor = ColumnTransformer(transformers=[
    ('num', numerical_pipeline, numerical_cols),
    ('cat', categorical_pipeline, categorical_cols)
], remainder='passthrough')

# Step 10: Apply Preprocessing
X_preprocessed = preprocessor.fit_transform(X)

# Step 11: Build Final Preprocessed DataFrame
X_preprocessed_df = pd.DataFrame(X_preprocessed)
final_full_df = pd.concat([X_preprocessed_df, y.reset_index(drop=True)], axis=1)

# Step 12: Apply KMeans Clustering
X_clustering = final_full_df.drop(columns=['SettlementValue'])
kmeans = KMeans(n_clusters=4, random_state=42)
cluster_labels = kmeans.fit_predict(X_clustering)

# Step 13: Add Cluster Column
final_full_df['Cluster'] = cluster_labels

# Step 14: Save Final Dataset
final_output_path = 'Synthetic_Data_Preprocessed_and_Clustered.csv'
final_full_df.to_csv(final_output_path, index=False)