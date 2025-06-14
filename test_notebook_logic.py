"""
Test the core logic that will be used in the evaluation notebook
"""

import os
import pandas as pd
import xgboost as xgb
import shap

def test_notebook_logic():
    """Test the evaluation notebook logic"""
    print("🧪 Testing Evaluation Notebook Logic...")
    print("=" * 50)
    
    # Test model loading
    print("\n1. Testing model loading...")
    try:
        MODEL_PATH = os.path.join("app", "ml", "predictor.bst")
        FEATURE_NAMES = ["pitch_strength_score", "identity_model_score", "momentum_tracker_score"]
        
        model = xgb.Booster()
        model.load_model(MODEL_PATH)
        print("✅ Model loaded successfully")
        
        explainer = shap.TreeExplainer(model)
        print("✅ SHAP explainer created")
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False
    
    # Test prediction function
    print("\n2. Testing prediction function...")
    try:
        def analyze_scenario_simple(scores: dict):
            input_df = pd.DataFrame([scores])[FEATURE_NAMES]
            dmatrix = xgb.DMatrix(input_df)
            
            # Prediction
            prediction_score = model.predict(dmatrix)[0]
            prediction_label = "Likely to Fund" if prediction_score > 0.5 else "Unlikely to Fund"
            
            # SHAP explanation
            shap_values = explainer(input_df)
            feature_impact = dict(zip(FEATURE_NAMES, shap_values.values[0]))
            
            return {
                'prediction_score': prediction_score,
                'prediction_label': prediction_label,
                'feature_impact': feature_impact
            }
        
        # Test with sample data
        test_scenario = {
            "pitch_strength_score": 8.5,
            "identity_model_score": 7.2,
            "momentum_tracker_score": 6.8
        }
        
        result = analyze_scenario_simple(test_scenario)
        print("✅ Prediction function working")
        print(f"   Score: {result['prediction_score']:.3f}")
        print(f"   Label: {result['prediction_label']}")
        print(f"   Feature impacts: {len(result['feature_impact'])} features")
        
    except Exception as e:
        print(f"❌ Prediction function failed: {e}")
        return False
    
    # Test multiple scenarios
    print("\n3. Testing multiple scenarios...")
    scenarios = [
        ("Strong Project", {"pitch_strength_score": 9.0, "identity_model_score": 8.5, "momentum_tracker_score": 7.5}),
        ("Weak Project", {"pitch_strength_score": 3.0, "identity_model_score": 4.0, "momentum_tracker_score": 2.5}),
        ("Moderate Project", {"pitch_strength_score": 6.0, "identity_model_score": 6.0, "momentum_tracker_score": 5.5})
    ]
    
    try:
        for name, scenario in scenarios:
            result = analyze_scenario_simple(scenario)
            print(f"   {name}: {result['prediction_score']:.3f} ({result['prediction_label']})")
        
        print("✅ Multiple scenarios tested successfully")
        
    except Exception as e:
        print(f"❌ Multiple scenarios test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Evaluation Notebook Logic Test PASSED!")
    print("\n📋 Notebook Features Verified:")
    print("  ✅ Model loading and initialization")
    print("  ✅ SHAP explainer creation")
    print("  ✅ Prediction function with explanations")
    print("  ✅ Multiple scenario analysis")
    print("  ✅ Feature impact calculations")
    
    print("\n📓 Ready for Jupyter Notebook execution!")
    return True

if __name__ == "__main__":
    success = test_notebook_logic()
    if success:
        print("\n✨ Notebook logic is solid and ready for demo!")
    else:
        print("\n❌ Please fix issues before proceeding.")
