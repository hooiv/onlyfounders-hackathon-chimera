# Project Chimera - OnlyFounders AI Hackathon Submission

**Track:** Track 3: Fundraise Prediction Agent
**Candidate:** ADITYA CHAUHAN
**Live Demo:** [Link to your Gradio/Streamlit app will go here later]
**Demo Video:** [Link to your YouTube/Vimeo video will go here later]

---

## 1. Project Goal

The objective of Project Chimera is to build a modular, secure, and explainable **Fundraise Prediction Agent**. This agent serves as a core component of the OnlyFounders AI swarm, designed to give investors a data-driven signal on a project's likelihood of successfully closing a funding round.

Our approach prioritizes the core judging criteria:
-   **Privacy-Preserving Architecture:** The agent is designed to run within a Trusted Execution Environment (TEE) and operates *only* on sanitized, numerical scores from other agents, never touching sensitive raw data.
-   **Technical Feasibility & Innovation:** We use a robust XGBoost model for prediction and a SHAP module for transparent, explainable scoring.
-   **Integration Readiness:** The agent is delivered as a clean, documented FastAPI endpoint, ready to be integrated into the OnlyFounders platform.

## 2. Architecture Diagram

Our agent is designed to be a central orchestrator, consuming privacy-preserving inputs from other specialized agents in the swarm.

![Architecture Diagram](docs/architecture_diagram.md)

## 3. Tech Stack

| Layer                  | Technology                                     | Justification                                                 |
| ---------------------- | ---------------------------------------------- | ------------------------------------------------------------- |
| **Backend Framework**  | FastAPI                                        | High performance, async support, and automatic API docs.      |
| **Machine Learning**   | XGBoost, Scikit-learn                          | Powerful gradient boosting for tabular data, industry standard. |
| **Explainability**     | SHAP (SHapley Additive exPlanations)           | Provides clear, model-agnostic explanations for each prediction. |
| **Privacy Design**     | TEE-Ready Architecture (e.g., Intel SGX)       | Ensures data and model confidentiality during execution.        |
| **Demo UI**            | Gradio                                         | Extremely fast way to build an interactive UI for an ML model.  |
| **Code & Environment** | Python, Pip, Venv                              | Standard, reproducible environment.                           |

## 4. Setup & Running the Project

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hooiv/onlyfounders-hackathon-chimera.git
cd onlyfounders-hackathon-chimera
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Train the model (optional - a pre-trained model will be provided):
```bash
python app/ml/train.py
```

5. Start the FastAPI server:
```bash
python app/main.py
```

The API will be available at `http://localhost:8000`

### API Documentation
Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.

## 5. Privacy-Preserving Design

### Core Privacy Principles

1. **Data Minimization**: Our agent only processes numerical scores (0-10 scale) from other agents, never raw sensitive data like pitch decks, founder identities, or proprietary business information.

2. **Trusted Execution Environment (TEE)**: The prediction logic is designed to run within a secure enclave, ensuring that even the model weights and intermediate computations remain confidential.

3. **Zero-Knowledge Integration**: We integrate with other agents through privacy-preserving protocols, receiving only the minimum necessary information to make predictions.

### Technical Implementation

- **Input Sanitization**: All inputs are validated and normalized to prevent data leakage
- **Secure Model Serving**: Model inference happens in isolation from external systems
- **Explainable Outputs**: SHAP values provide transparency without exposing sensitive model internals

## 6. Model Performance & Validation

(Detailed metrics will be added after model training and validation)

## 7. Integration Guide

### API Endpoints

#### POST /predict
Accepts privacy-preserving scores and returns explainable predictions.

**Request Body:**
```json
{
  "pitch_score": 8.5,
  "trust_score": 7.2,
  "momentum_score": 6.8
}
```

**Response:**
```json
{
  "prediction_score": 0.82,
  "prediction_label": "Likely to Fund",
  "key_drivers": [
    "High Pitch Strength",
    "Strong Founder Trust"
  ]
}
```

## 8. Future Enhancements

- Integration with additional privacy-preserving agents
- Advanced ensemble methods for improved accuracy
- Real-time model updates with federated learning
- Enhanced explainability with counterfactual analysis

## 9. License

This project is developed for the OnlyFounders AI Hackathon.

---

**Contact:** 125276621+hooiv@users.noreply.github.com