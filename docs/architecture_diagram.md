# Project Chimera: Fundraise Prediction Agent Architecture

This document contains the architecture diagram for Project Chimera.

## Mermaid Diagram Code

```mermaid
graph LR
    subgraph "Inputs (Privacy-Preserving Scores)"
        A1["Track 2: Pitch Strength Agent<br/>Runs locally on user's device<br/>Processes sensitive pitch deck"]
        A2["Track 1: Identity Model Agent<br/>Uses ZK-proofs to verify founder<br/>reputation without revealing identity"]
        A3["Track 6: Momentum Tracker Agent<br/>Federated analysis of public<br/>GitHub/Twitter data"]
    end
    
    subgraph "Core Agent Logic (TEE)" 
        subgraph TEE["Our Agent: Track 3<br/>(Running inside Trusted Execution Environment)"]
            B1["Input Validation &<br/>Preprocessing"]
            B2["XGBoost Prediction<br/>Model"]
            B3["SHAP Explainability<br/>Module"]
            B1 --> B2
            B2 --> B3
        end
    end
    
    subgraph "Outputs (Explainable Prediction)"
        C1["API Response (JSON)<br/>{<br/>  'prediction_score': 0.82,<br/>  'prediction_label': 'Likely to Fund',<br/>  'key_drivers': [<br/>    'High Pitch Strength',<br/>    'Strong Founder Trust'<br/>  ]<br/>}"]
    end
    
    A1 -->|"{'pitch_score': 8.5}"| B1
    A2 -->|"{'trust_score': 7.2}"| B1
    A3 -->|"{'momentum_score': 6.8}"| B1
    B3 --> C1
    
    style TEE stroke-dasharray: 5 5
    style A1 fill:#e1f5fe
    style A2 fill:#e1f5fe
    style A3 fill:#e1f5fe
    style TEE fill:#fff3e0
    style C1 fill:#e8f5e8
```

## Architecture Description

### Column 1: Inputs (Privacy-Preserving Scores)
- **Track 2: Pitch Strength Agent**: Runs locally on user's device, processes sensitive pitch deck
- **Track 1: Identity Model Agent**: Uses ZK-proofs to verify founder reputation without revealing identity  
- **Track 6: Momentum Tracker Agent**: Federated analysis of public GitHub/Twitter data

### Column 2: Core Agent Logic (TEE)
- **Our Agent: Track 3**: Running inside a Trusted Execution Environment (TEE)
  - Input Validation & Preprocessing
  - XGBoost Prediction Model
  - SHAP Explainability Module

### Column 3: Outputs (Explainable Prediction)
- **API Response**: JSON format with prediction score, label, and key drivers

## Key Design Principles

1. **Privacy-Preserving**: Only processes sanitized numerical scores, never raw sensitive data
2. **Secure Execution**: Runs within a TEE to ensure data and model confidentiality
3. **Explainable**: Uses SHAP to provide transparent reasoning for predictions
4. **Integration Ready**: Clean API interface for seamless platform integration
