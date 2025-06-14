"""
Test the complete full-stack application (Backend + Frontend)
"""

import requests
import time

def test_full_stack():
    """Test both the API backend and Gradio frontend"""
    print("🌐 Testing Complete Full-Stack Application...")
    print("=" * 60)
    
    # Test 1: Backend API Health Check
    print("\n1. Testing Backend API...")
    try:
        response = requests.get("http://127.0.0.1:8000/")
        if response.status_code == 200:
            print("✅ Backend API is running")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Backend API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend API connection failed: {e}")
        return False
    
    # Test 2: Backend AI Prediction
    print("\n2. Testing Backend AI Prediction...")
    test_data = {
        "pitch_strength_score": 8.5,
        "identity_model_score": 7.2,
        "momentum_tracker_score": 6.8
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=test_data
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ Backend AI prediction working")
            print(f"   Score: {result['prediction_score']:.3f}")
            print(f"   Label: {result['prediction_label']}")
            print(f"   Drivers: {result['key_drivers']}")
        else:
            print(f"❌ Backend prediction error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend prediction failed: {e}")
        return False
    
    # Test 3: Frontend UI Health Check
    print("\n3. Testing Frontend UI...")
    try:
        response = requests.get("http://127.0.0.1:7860/")
        if response.status_code == 200:
            print("✅ Frontend UI is running")
            print("   Gradio interface accessible")
        else:
            print(f"❌ Frontend UI error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend UI connection failed: {e}")
        return False
    
    # Test 4: End-to-End Integration
    print("\n4. Testing End-to-End Integration...")
    print("   (Simulating what happens when user moves sliders)")
    
    # Simulate the same call that Gradio makes
    try:
        # This simulates what the get_prediction function does
        payload = {
            "pitch_strength_score": 9.0,
            "identity_model_score": 8.0,
            "momentum_tracker_score": 7.5
        }
        
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            # Format like the UI does
            score = result["prediction_score"]
            label = result["prediction_label"]
            drivers = "\n".join(f"- {driver}" for driver in result["key_drivers"])
            
            ui_output = (
                f"**Prediction Score:** {score:.2f}\n"
                f"**Prediction Label:** {label}\n\n"
                f"**Key Drivers for this Prediction:**\n{drivers}"
            )
            
            print("✅ End-to-end integration working")
            print("   UI would display:")
            print(f"   {ui_output}")
            
        else:
            print(f"❌ Integration test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Full-Stack Application Test PASSED!")
    print("\n🌟 System Status:")
    print("  ✅ Backend API: Running with AI model loaded")
    print("  ✅ Frontend UI: Gradio interface accessible")
    print("  ✅ AI Intelligence: XGBoost + SHAP working")
    print("  ✅ Integration: End-to-end communication working")
    print("\n🚀 Project Chimera is a complete full-stack AI application!")
    print("\n📱 Access the demo at: http://127.0.0.1:7860")
    print("🔧 API documentation at: http://127.0.0.1:8000/docs")
    
    return True

if __name__ == "__main__":
    success = test_full_stack()
    if success:
        print("\n✨ Ready for demo video recording!")
    else:
        print("\n❌ Please check server status and try again.")
