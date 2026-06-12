# ML Models

## Model 1: Risk Classifier
- **Output:** Low / Medium / High risk label
- **Algorithms:** Random Forest + XGBoost (compare both, keep best)
- **Metrics:** F1-score, Accuracy, Confusion Matrix
- **File:** models/risk_classifier.pkl

## Model 2: Incident Count Regressor
- **Output:** Expected incident count for area + time window
- **Algorithms:** Random Forest + XGBoost Regressor
- **Metrics:** MAE, RMSE, R² score
- **File:** models/incident_regressor.pkl

## Model 3: Route Risk Score (Formula-based, no .pkl needed)
```
Route Risk Score =
  average area risk score
  + hotspot proximity penalty
  + night-time risk multiplier
  + persona weight adjustment
  + emergency distance penalty
  + community signal penalty
```

## Training Data
- Source: NCRB crime data (processed/safescope_dataset.csv)
- 25 feature columns → see data/README.md for full list
- Train/test split: 80/20

TODO: Fill in actual metric numbers after Day 7-8 training runs.
