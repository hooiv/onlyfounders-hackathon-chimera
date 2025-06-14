"""
Project Chimera - Quick Demo Script
Track 3: Fundraise Prediction Agent

This script demonstrates the core functionality without requiring full dependencies.
"""

import json
from typing import Dict, List, Tuple

class ChimeraDemo:
    """Simplified demo version of the Chimera prediction agent"""
    
    def __init__(self):
        self.feature_names = ['pitch_score', 'trust_score', 'momentum_score']
        self.weights = [0.4, 0.35, 0.25]  # Feature importance weights
    
    def validate_input(self, input_data: Dict[str, float]) -> bool:
        """Validate input data"""
        for feature in self.feature_names:
            if feature not in input_data:
                print(f"❌ Missing required feature: {feature}")
                return False
            
            score = input_data[feature]
            if not 0 <= score <= 10:
                print(f"⚠️  Warning: {feature} = {score} is outside expected range [0, 10]")
        
        return True
    
    def predict(self, input_data: Dict[str, float]) -> Tuple[float, str]:
        """Generate prediction"""
        if not self.validate_input(input_data):
            return 0.0, "Invalid Input"
        
        # Weighted average with normalization
        weighted_score = sum(
            input_data[feature] * weight 
            for feature, weight in zip(self.feature_names, self.weights)
        ) / 10.0
        
        # Add some non-linearity for realism
        if weighted_score >= 0.8:
            weighted_score = min(0.95, weighted_score * 1.1)
        elif weighted_score <= 0.3:
            weighted_score = max(0.05, weighted_score * 0.8)
        
        # Determine label
        if weighted_score >= 0.7:
            label = "Likely to Fund"
        elif weighted_score >= 0.5:
            label = "Moderate Potential"
        else:
            label = "Low Funding Probability"
        
        return round(weighted_score, 2), label
    
    def explain_prediction(self, input_data: Dict[str, float]) -> List[str]:
        """Generate explanation for the prediction"""
        scores = [(name, input_data[name]) for name in self.feature_names]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        explanations = []
        for feature_name, score in scores[:2]:
            if feature_name == 'pitch_score':
                if score >= 7:
                    explanations.append("High Pitch Strength")
                elif score >= 5:
                    explanations.append("Moderate Pitch Quality")
                else:
                    explanations.append("Pitch Needs Improvement")
            elif feature_name == 'trust_score':
                if score >= 7:
                    explanations.append("Strong Founder Trust")
                elif score >= 5:
                    explanations.append("Moderate Founder Credibility")
                else:
                    explanations.append("Trust Building Needed")
            else:  # momentum_score
                if score >= 7:
                    explanations.append("Strong Market Momentum")
                elif score >= 5:
                    explanations.append("Moderate Traction")
                else:
                    explanations.append("Limited Market Traction")
        
        return explanations
    
    def process_request(self, input_data: Dict[str, float]) -> Dict:
        """Process a complete prediction request"""
        prediction_score, prediction_label = self.predict(input_data)
        key_drivers = self.explain_prediction(input_data)
        
        return {
            "prediction_score": prediction_score,
            "prediction_label": prediction_label,
            "key_drivers": key_drivers,
            "input_scores": input_data
        }

def run_demo():
    """Run the demo with sample data"""
    print("🚀 Project Chimera - Fundraise Prediction Agent Demo")
    print("=" * 60)
    
    # Initialize the demo agent
    agent = ChimeraDemo()
    
    # Test cases
    test_cases = [
        {
            "name": "High-Potential Startup",
            "data": {"pitch_score": 8.5, "trust_score": 7.2, "momentum_score": 6.8}
        },
        {
            "name": "Moderate Startup",
            "data": {"pitch_score": 6.0, "trust_score": 5.5, "momentum_score": 5.0}
        },
        {
            "name": "Early-Stage Startup",
            "data": {"pitch_score": 4.5, "trust_score": 6.0, "momentum_score": 3.2}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📊 Test Case {i}: {test_case['name']}")
        print("-" * 40)
        
        # Show input
        print("Input Scores:")
        for feature, score in test_case['data'].items():
            print(f"  • {feature.replace('_', ' ').title()}: {score}/10")
        
        # Get prediction
        result = agent.process_request(test_case['data'])
        
        # Show output
        print(f"\n🎯 Prediction: {result['prediction_label']}")
        print(f"📈 Confidence Score: {result['prediction_score']}")
        print("🔍 Key Drivers:")
        for driver in result['key_drivers']:
            print(f"  • {driver}")
        
        # Show as JSON (API format)
        print(f"\n📋 API Response:")
        api_response = {
            "prediction_score": result['prediction_score'],
            "prediction_label": result['prediction_label'],
            "key_drivers": result['key_drivers']
        }
        print(json.dumps(api_response, indent=2))
    
    print("\n" + "=" * 60)
    print("✅ Demo completed successfully!")
    print("\n🔗 Architecture Highlights:")
    print("  • Privacy-Preserving: Only processes numerical scores")
    print("  • TEE-Ready: Designed for secure execution environments")
    print("  • Explainable: Clear reasoning for each prediction")
    print("  • Integration-Ready: Clean JSON API interface")

if __name__ == "__main__":
    run_demo()
