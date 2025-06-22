# Project Chimera - OnlyFounders AI Hackathon Submission

**Track:** Track 3: Fundraise Prediction Agent
**Candidate:** ADITYA CHAUHAN
**Demo:** can be run locally via `demo_ui.py`.
**Demo Video:** https://youtu.be/j4Vm3hTxcr8
**Evaluation Notebook:** You can view the [evaluation_notebook.ipynb](evaluation_notebook.ipynb) directly in GitHub.

---

## 1. Project Goal

The objective of Project Chimera is to build a modular, secure, and explainable **Fundraise Prediction Agent**. This agent serves as a core component of the OnlyFounders AI swarm, designed to give investors a data-driven signal on a project's likelihood of successfully closing a funding round.

My approach prioritizes the core judging criteria:

-   **Privacy-Preserving Architecture:** The agent is designed to run within a Trusted Execution Environment (TEE). It operates *only* on sanitized, numerical scores from other agents, never touching sensitive raw data like pitch decks or personal information. This respects data sovereignty by design.
-   **Technical Feasibility & Innovation:** We use a robust XGBoost model for its performance and a SHAP module for transparent, model-agnostic explainability. The agent is not a black box; it provides the "why" behind every prediction.
-   **Usability & Integration Readiness:** The agent is delivered as a clean, well-documented FastAPI endpoint. Its modular nature (accepting scores as input) makes it simple to plug into the OnlyFounders platform.
-   **Documentation & Presentation:** The project is cleanly structured, fully documented, and presented in a concise demo video.

## 2. Architecture Diagram

Our agent is designed to be a central orchestrator, consuming privacy-preserving inputs from other specialized agents in the swarm. This separation of concerns is key to a scalable and secure multi-agent system.

![Architecture Diagram](docs/architecture_diagram.md)

## 3. Tech Stack

| Layer                  | Technology                                     | Justification                                                 |
| ---------------------- | ---------------------------------------------- | ------------------------------------------------------------- |
| **Backend Framework**  | FastAPI                                        | High performance, async support, and automatic API docs.      |
| **Machine Learning**   | XGBoost, Scikit-learn, Pandas                  | Powerful gradient boosting for tabular data; industry standard. |
| **Explainability**     | SHAP (SHapley Additive exPlanations)           | Provides clear, model-agnostic explanations for each prediction. |
| **Privacy Design**     | TEE-Ready Architecture (e.g., Intel SGX)       | The stateless, self-contained design is built to be deployed in a secure enclave. |
| **Interactive Demo**   | Gradio                                         | Extremely fast way to build an impressive UI for an ML model.   |
| **Code & Environment** | Python 3.9+, Pip, Venv                           | Standard, reproducible development environment.                 |

## 4. Setup & Running the Project

To run this project locally, please follow these steps.

### Prerequisites

-   Python 3.9+
-   `pip` and `venv`

### Step 1: Clone the Repository

```bash
git clone https://github.com/hooiv/onlyfounders-hackathon-chimera.git
cd onlyfounders-hackathon-chimera
```

### Step 2: Set Up the Python Environment
```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install all required packages
pip install -r requirements.txt
```

### Step 3: Train the Model (First-Time Setup)

The model is included, but you can retrain it by running:

```bash
python app/ml/train.py
```

### Step 4: Run the Application

You need two terminals to run the backend API and the frontend UI.

In Terminal 1, start the backend API:

```bash
uvicorn app.main:app
```

In Terminal 2, start the Gradio UI:

```bash
python demo_ui.py
```

Now, open your browser and navigate to the local URL provided by Gradio (usually http://127.0.0.1:7860).

## 5. Privacy-Preserving Design

Privacy is not an afterthought in this project; it is the foundation of the architecture.

**No Raw Data Processing:** The Chimera agent never receives sensitive information. It does not see pitch decks, founder wallet addresses, or any other private data. Its sole function is to process anonymized, numerical scores.

**Defined Trust Boundary:** The architecture clearly defines a trust boundary. The sensitive work of processing raw data is delegated to other agents (e.g., a local Pitch Scorer), which are responsible for producing the privacy-preserving scores.

**Built for TEEs:** The application logic is stateless and self-contained, making it perfectly suited for deployment within a Trusted Execution Environment like Intel SGX or Azure DCsv3. This would provide hardware-level guarantees that the model and its operations are completely isolated and confidential.

## 6. Model Performance & Validation

### Technical Specifications
- **Algorithm**: XGBoost Classifier
- **Training Accuracy**: 83%
- **Dataset**: 1000 synthetic samples with realistic correlations
- **Features**: 3 privacy-preserving numerical scores (0-10 scale)
- **Explainability**: SHAP TreeExplainer for transparent reasoning

### Key Performance Metrics
- **Balanced Performance**: 83% accuracy across both funded/not-funded classes
- **Feature Importance**: Pitch strength (primary), Identity trust (secondary), Momentum (supporting)
- **Prediction Confidence**: Dynamic scoring from 1.5% to 99.6% based on input quality
- **Real-time Performance**: Sub-second predictions suitable for production deployment

## 7. Integration Guide

### API Endpoints

#### POST /predict
Accepts privacy-preserving scores and returns explainable predictions.

**Request Body:**
```json
{
  "pitch_strength_score": 8.5,
  "identity_model_score": 7.2,
  "momentum_tracker_score": 6.8
}
```

**Response:**
```json
{
  "prediction_score": 0.996,
  "prediction_label": "Likely to Fund",
  "key_drivers": [
    "Impact of Pitch Strength Score",
    "Impact of Identity Model Score"
  ]
}
```

#### GET /
Health check endpoint returning server status.

#### GET /docs
Interactive API documentation (Swagger UI) for testing and integration.

### Integration Benefits
- **Modular Design**: Clean separation from other swarm agents
- **API-First**: RESTful interface for easy platform integration
- **Scalable**: Efficient model loading and prediction pipeline
- **Secure**: TEE-compatible for confidential execution
- **Documented**: Automatic OpenAPI documentation generation

## 8. Demo & Evaluation

### Interactive Demo
Run `python demo_ui.py` to launch the Gradio interface featuring:
- **Real-time Predictions**: Instant updates as you adjust input sliders
- **Explainable AI**: SHAP key drivers displayed for every prediction
- **Professional UI**: Clean, impressive interface perfect for demonstrations
- **Multiple Scenarios**: Test various startup profiles and see dynamic results

### Evaluation Notebook
The `evaluation_notebook.ipynb` provides comprehensive model analysis:
- **Scenario Testing**: Multiple startup profiles with detailed explanations
- **SHAP Visualizations**: Feature impact plots and force diagrams
- **Performance Analysis**: Model behavior across different input combinations
- **Self-contained**: Runs independently without requiring the API server

## 9. Future Enhancements

- **Enhanced Privacy**: Integration with additional ZK-proof and federated learning techniques
- **Advanced ML**: Ensemble methods and continuous learning capabilities
- **Platform Integration**: Direct OnlyFounders platform API integration
- **Scalability**: Kubernetes deployment and auto-scaling configurations
- **Monitoring**: Comprehensive logging and performance monitoring

---

**Thank you for considering my submission.**

**Contact:** 125276621+hooiv@users.noreply.github.com
**GitHub:** https://github.com/hooiv/onlyfounders-hackathon-chimera