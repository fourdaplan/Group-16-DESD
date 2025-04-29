import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

file_path = 'Synthetic_Data_For_Students (2).csv'
df_full = pd.read_csv(file_path)

df_full['Accident Date'] = pd.to_datetime(df_full['Accident Date'], errors='coerce', format='%d/%m/%Y')
df_full['Claim Date'] = pd.to_datetime(df_full['Claim Date'], errors='coerce', format='%d/%m/%Y')
df_full['Days_To_Claim'] = (df_full['Claim Date'] - df_full['Accident Date']).dt.days
df_full = df_full.drop(columns=['Accident Date', 'Claim Date'])

bool_cols = ['Police Report Filed', 'Witness Present', 'Whiplash', 'Exceptional_Circumstances', 'Minor_Psychological_Injury']
for col in bool_cols:
    if col in df_full.columns:
        df_full[col] = df_full[col].map({'Yes': 1, 'No': 0})

text_cols = ['Accident Description', 'Injury Description']
for col in text_cols:
    if col in df_full.columns:
        df_full[col] = df_full[col].fillna('Missing')

target_col = 'SettlementValue'
df_full = df_full[df_full[target_col].notna()]
y = df_full[target_col].reset_index(drop=True)
X = df_full.drop(columns=[target_col])

numerical_cols = X.select_dtypes(include=['float64', 'int64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

def label_encode_dataframe(X_cat):
    X_cat = pd.DataFrame(X_cat)
    encoded = pd.DataFrame()
    for col in X_cat.columns:
        le = LabelEncoder()
        X_cat[col] = X_cat[col].fillna('Missing')
        encoded[col] = le.fit_transform(X_cat[col])
    return encoded.values

numerical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('label_encoder', FunctionTransformer(label_encode_dataframe, validate=False))
])

preprocessor = ColumnTransformer([
    ('num', numerical_pipeline, numerical_cols),
    ('cat', categorical_pipeline, categorical_cols)
])

X_preprocessed = preprocessor.fit_transform(X)
X_preprocessed_df = pd.DataFrame(X_preprocessed)
X_preprocessed_df.columns = X_preprocessed_df.columns.astype(str)

X_preprocessed_df['SettlementValue'] = y
final_output_path = 'Synthetic_Data_Preprocessed.csv'
X_preprocessed_df.to_csv(final_output_path, index=False)
