"""
Project Chimera - Model Logic
Track 3: Fundraise Prediction Agent

This module contains the machine learning model loading and prediction logic.
"""

import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import shap
from pathlib import Path

class FundraisePredictionModel:
    """
    Main prediction model class for fundraise prediction.
    
    This class handles:
    - Model loading and initialization
    - Input preprocessing and validation
    - Prediction generation
    - SHAP-based explainability
    """
    
    def __init__(self, model_path: str = None):
        """Initialize the prediction model"""
        self.model = None
        self.explainer = None
        self.feature_names = ['pitch_score', 'trust_score', 'momentum_score']
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
        else:
            # Initialize with a simple baseline model for demo purposes
            self._initialize_baseline_model()
    
    def _initialize_baseline_model(self):
        """Initialize a simple baseline model for demonstration"""
        # This is a placeholder - in production, this would load a trained XGBoost model
        print("Initializing baseline model (placeholder)")
        
    def load_model(self, model_path: str):
        """Load a trained model from disk"""
        try:
            self.model = joblib.load(model_path)
            # Initialize SHAP explainer
            # self.explainer = shap.TreeExplainer(self.model)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self._initialize_baseline_model()
    
    def preprocess_input(self, input_data: Dict[str, float]) -> np.ndarray:
        """
        Preprocess and validate input data
        
        Args:
            input_data: Dictionary with pitch_score, trust_score, momentum_score
            
        Returns:
            Preprocessed numpy array ready for prediction
        """
        # Validate input
        required_features = self.feature_names
        for feature in required_features:
            if feature not in input_data:
                raise ValueError(f"Missing required feature: {feature}")
        
        # Extract features in correct order
        features = [input_data[feature] for feature in required_features]
        
        # Validate score ranges (should be 0-10)
        for i, score in enumerate(features):
            if not 0 <= score <= 10:
                print(f"Warning: {required_features[i]} = {score} is outside expected range [0, 10]")
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, input_data: Dict[str, float]) -> Tuple[float, str]:
        """
        Generate prediction for fundraise success
        
        Args:
            input_data: Dictionary with input scores
            
        Returns:
            Tuple of (prediction_score, prediction_label)
        """
        # Preprocess input
        X = self.preprocess_input(input_data)
        
        if self.model is not None:
            # Use trained model
            prediction_score = float(self.model.predict_proba(X)[0][1])
        else:
            # Use baseline logic
            prediction_score = self._baseline_prediction(input_data)
        
        # Convert to label
        if prediction_score >= 0.7:
            label = "Likely to Fund"
        elif prediction_score >= 0.5:
            label = "Moderate Potential"
        else:
            label = "Low Funding Probability"
        
        return prediction_score, label
    
    def _baseline_prediction(self, input_data: Dict[str, float]) -> float:
        """Simple baseline prediction logic"""
        # Weighted average with some non-linearity
        weighted_score = (
            input_data['pitch_score'] * 0.4 +
            input_data['trust_score'] * 0.35 +
            input_data['momentum_score'] * 0.25
        ) / 10.0
        
        # Add some non-linearity
        if weighted_score >= 0.8:
            weighted_score = min(0.95, weighted_score * 1.1)
        elif weighted_score <= 0.3:
            weighted_score = max(0.05, weighted_score * 0.8)
        
        return weighted_score
    
    def explain_prediction(self, input_data: Dict[str, float]) -> List[str]:
        """
        Generate explanation for the prediction using SHAP or simple logic
        
        Args:
            input_data: Dictionary with input scores
            
        Returns:
            List of key drivers for the prediction
        """
        if self.explainer is not None:
            # Use SHAP for explanation
            X = self.preprocess_input(input_data)
            shap_values = self.explainer.shap_values(X)
            
            # Get feature importance
            feature_importance = list(zip(self.feature_names, shap_values[0]))
            feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)
            
            # Generate explanations
            explanations = []
            for feature, importance in feature_importance[:2]:
                if feature == 'pitch_score':
                    explanations.append("High Pitch Strength" if importance > 0 else "Weak Pitch")
                elif feature == 'trust_score':
                    explanations.append("Strong Founder Trust" if importance > 0 else "Trust Concerns")
                else:
                    explanations.append("Strong Momentum" if importance > 0 else "Limited Momentum")
            
            return explanations
        else:
            # Use simple rule-based explanation
            return self._simple_explanation(input_data)
    
    def _simple_explanation(self, input_data: Dict[str, float]) -> List[str]:
        """Simple rule-based explanation"""
        scores = [
            ('pitch_score', input_data['pitch_score'], 'Pitch Strength'),
            ('trust_score', input_data['trust_score'], 'Founder Trust'),
            ('momentum_score', input_data['momentum_score'], 'Market Momentum')
        ]
        
        # Sort by score value
        scores.sort(key=lambda x: x[1], reverse=True)
        
        explanations = []
        for _, score, name in scores[:2]:
            if score >= 7:
                explanations.append(f"High {name}")
            elif score >= 5:
                explanations.append(f"Moderate {name}")
            else:
                explanations.append(f"Low {name}")
        
        return explanations
