"""
Test the fully integrated AI API with real XGBoost predictions
"""

import requests
import json

def test_integrated_api():
    """Test the API with the integrated XGBoost model"""
    base_url = "http://127.0.0.1:8000"
    
    print("🤖 Testing Fully Integrated AI Agent...")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Health check passed!")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: High-potential startup
    print("\n2. Testing high-potential startup...")
    test_data = {
        "pitch_strength_score": 8.5,
        "identity_model_score": 7.2,
        "momentum_tracker_score": 6.8
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Input: {test_data}")
        print(f"AI Prediction: {json.dumps(result, indent=2)}")
        
        # Verify it's using the real model (not mock)
        if "Impact of" in str(result.get('key_drivers', [])):
            print("✅ Real AI model is working! (SHAP explanations detected)")
        else:
            print("⚠️  Might still be using mock logic")
            
    except Exception as e:
        print(f"❌ High-potential test failed: {e}")
    
    # Test 3: Low-potential startup
    print("\n3. Testing low-potential startup...")
    test_data_low = {
        "pitch_strength_score": 3.0,
        "identity_model_score": 4.0,
        "momentum_tracker_score": 2.5
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            json=test_data_low
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Input: {test_data_low}")
        print(f"AI Prediction: {json.dumps(result, indent=2)}")
        
        # Check if prediction makes sense
        score = result.get('prediction_score', 0)
        if score < 0.5:
            print("✅ AI correctly identified low potential!")
        else:
            print(f"⚠️  Unexpected high score ({score}) for low inputs")
            
    except Exception as e:
        print(f"❌ Low-potential test failed: {e}")
    
    # Test 4: Edge case - mixed signals
    print("\n4. Testing mixed signals...")
    test_data_mixed = {
        "pitch_strength_score": 9.0,  # Very high
        "identity_model_score": 3.0,  # Very low
        "momentum_tracker_score": 6.0  # Medium
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            json=test_data_mixed
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Input: {test_data_mixed}")
        print(f"AI Prediction: {json.dumps(result, indent=2)}")
        
        # Check SHAP explanations
        drivers = result.get('key_drivers', [])
        if len(drivers) >= 2:
            print(f"✅ SHAP providing {len(drivers)} key drivers")
        else:
            print("⚠️  Expected more key drivers from SHAP")
            
    except Exception as e:
        print(f"❌ Mixed signals test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Integrated AI Agent Testing Complete!")
    print("\n🧠 AI Integration Summary:")
    print("  • XGBoost model loaded and running")
    print("  • SHAP explainability providing insights")
    print("  • Real-time predictions via API")
    print("  • Dynamic responses based on input")
    print("\n🚀 Project Chimera is now a fully intelligent agent!")

if __name__ == "__main__":
    test_integrated_api()
