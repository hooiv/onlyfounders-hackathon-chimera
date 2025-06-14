"""
Test script for Project Chimera API
"""

import requests
import json

def test_api():
    """Test the FastAPI server endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Project Chimera API...")
    print("=" * 50)
    
    # Test 1: Health check endpoint
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Health check passed!")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Prediction endpoint with high scores
    print("\n2. Testing prediction endpoint (high scores)...")
    test_data_high = {
        "pitch_strength_score": 8.5,
        "identity_model_score": 7.2,
        "momentum_tracker_score": 6.8
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            json=test_data_high
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Input: {test_data_high}")
        print(f"Response: {json.dumps(result, indent=2)}")
        print("✅ High score prediction passed!")
    except Exception as e:
        print(f"❌ High score prediction failed: {e}")
    
    # Test 3: Prediction endpoint with low scores
    print("\n3. Testing prediction endpoint (low scores)...")
    test_data_low = {
        "pitch_strength_score": 4.5,
        "identity_model_score": 5.0,
        "momentum_tracker_score": 3.2
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            json=test_data_low
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Input: {test_data_low}")
        print(f"Response: {json.dumps(result, indent=2)}")
        print("✅ Low score prediction passed!")
    except Exception as e:
        print(f"❌ Low score prediction failed: {e}")
    
    # Test 4: Invalid input validation
    print("\n4. Testing input validation...")
    invalid_data = {
        "pitch_strength_score": 15.0,  # Invalid: > 10
        "identity_model_score": -2.0,  # Invalid: < 0
        "momentum_tracker_score": 6.8
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            json=invalid_data
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 422:
            print("✅ Input validation working correctly!")
            print(f"Validation Error: {response.json()}")
        else:
            print(f"⚠️  Unexpected response: {response.json()}")
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("\n📋 Next steps:")
    print("- Visit http://127.0.0.1:8000/docs for interactive API documentation")
    print("- The server is ready for Day 3 model integration")

if __name__ == "__main__":
    test_api()
