# Core Model

This module contains a two-level prediction system for estimating compensation settlement values.

## Structure

- `train.py`: Main training pipeline
- `model_router.py`: Maps group ID to regression model
- `explainer.py`: Generates SHAP visualizations
- `predict.py`: Runs trained models for inference

## Requirements

- scikit-learn
- pandas
- joblib
- shap
- matplotlib

## Training

Place the dataset `Synthetic_Data_Preprocessed_and_Clustered.csv` in the root.
Then run:
```bash
python mlaas_service/core_model/train.py

```

Models and SHAP plots will be saved under `core_model/`.
