"""
Project Chimera - Model Training Script
Track 3: Fundraise Prediction Agent

This script trains the XGBoost model for fundraise prediction.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import xgboost as xgb
import joblib
import shap
from pathlib import Path

def generate_synthetic_data(n_samples: int = 1000) -> pd.DataFrame:
    """
    Generate synthetic training data for demonstration purposes.
    
    In a real implementation, this would be replaced with actual
    historical fundraising data.
    """
    np.random.seed(42)
    
    # Generate correlated features
    pitch_scores = np.random.normal(6.5, 2.0, n_samples)
    trust_scores = np.random.normal(6.0, 1.8, n_samples)
    momentum_scores = np.random.normal(5.5, 2.2, n_samples)
    
    # Clip to valid range
    pitch_scores = np.clip(pitch_scores, 0, 10)
    trust_scores = np.clip(trust_scores, 0, 10)
    momentum_scores = np.clip(momentum_scores, 0, 10)
    
    # Generate target variable with realistic relationships
    # Higher scores should generally lead to higher funding probability
    funding_probability = (
        0.4 * (pitch_scores / 10) +
        0.35 * (trust_scores / 10) +
        0.25 * (momentum_scores / 10)
    )
    
    # Add some noise and non-linearity
    noise = np.random.normal(0, 0.1, n_samples)
    funding_probability += noise
    
    # Apply sigmoid-like transformation for realism
    funding_probability = 1 / (1 + np.exp(-5 * (funding_probability - 0.5)))
    
    # Convert to binary labels (funded vs not funded)
    # Use a threshold that gives roughly 30% positive class
    threshold = np.percentile(funding_probability, 70)
    funded = (funding_probability > threshold).astype(int)
    
    # Create DataFrame
    data = pd.DataFrame({
        'pitch_score': pitch_scores,
        'trust_score': trust_scores,
        'momentum_score': momentum_scores,
        'funding_probability': funding_probability,
        'funded': funded
    })
    
    return data

def train_model(data: pd.DataFrame) -> xgb.XGBClassifier:
    """
    Train the XGBoost model
    """
    # Prepare features and target
    feature_columns = ['pitch_score', 'trust_score', 'momentum_score']
    X = data[feature_columns]
    y = data['funded']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train XGBoost model
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric='logloss'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    print("Model Performance:")
    print(f"ROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
    print(f"\nCross-validation ROC AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    return model

def save_model(model: xgb.XGBClassifier, model_path: str):
    """Save the trained model"""
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

def main():
    """Main training pipeline"""
    print("Starting model training for Project Chimera...")
    
    # Generate synthetic data
    print("Generating synthetic training data...")
    data = generate_synthetic_data(n_samples=2000)
    
    print(f"Dataset shape: {data.shape}")
    print(f"Positive class ratio: {data['funded'].mean():.2%}")
    
    # Train model
    print("\nTraining XGBoost model...")
    model = train_model(data)
    
    # Save model
    model_path = "app/ml/predictor.bst"
    save_model(model, model_path)
    
    # Feature importance
    print("\nFeature Importance:")
    feature_names = ['pitch_score', 'trust_score', 'momentum_score']
    importance_scores = model.feature_importances_
    
    for name, importance in zip(feature_names, importance_scores):
        print(f"{name}: {importance:.3f}")
    
    print("\nModel training completed successfully!")

if __name__ == "__main__":
    main()
