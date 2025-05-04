# preprocess.py

import pandas as pd

def load_and_preprocess(filepath):
    df = pd.read_csv(filepath)

    # Dates & derived features
    df['Accident Date'] = pd.to_datetime(df['Accident Date'], errors='coerce', format='%d/%m/%Y')
    df['Claim Date'] = pd.to_datetime(df['Claim Date'], errors='coerce', format='%d/%m/%Y')
    df['Days_To_Claim'] = (df['Claim Date'] - df['Accident Date']).dt.days
    df.drop(columns=['Accident Date', 'Claim Date'], inplace=True)

    # Binary encoding
    bool_cols = ['Police Report Filed', 'Witness Present', 'Whiplash', 'Exceptional_Circumstances', 'Minor_Psychological_Injury']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0})

    # Fill missing text
    text_cols = ['Accident Description', 'Injury Description']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Missing')

    # Drop NaNs in target
    df = df[df['SettlementValue'].notna()]

    # Define target and features
    y = df['SettlementValue'].reset_index(drop=True)
    X = df.drop(columns=['SettlementValue'])
    X['Description_Length'] = X['Accident Description'].apply(lambda x: len(str(x).split()))

    return X, y
