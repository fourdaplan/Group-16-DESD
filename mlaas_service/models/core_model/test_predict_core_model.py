from predict import make_prediction
import pandas as pd

sample_data = pd.read_csv("your_new_data.csv")  # Must match preprocessing format
preds = make_prediction(sample_data)
print(preds)
