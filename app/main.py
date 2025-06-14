from fastapi import FastAPI
from pydantic import BaseModel, Field

# --- 1. DEFINE THE API ---
# Create a FastAPI instance. This is the main point of interaction for our API.
# The title and version will show up in the auto-generated documentation.
app = FastAPI(
    title="Project Chimera: Fundraise Prediction Agent",
    version="1.0",
    description="A privacy-preserving AI agent to predict startup fundraising success."
)


# --- 2. DEFINE THE INPUT DATA MODEL ---
# Pydantic models give us data validation and typing for free.
# This defines the exact structure of the JSON we expect to receive.
# 'Field' allows us to add validation rules, e.g., scores must be between 0 and 10.
class AgentInput(BaseModel):
    pitch_strength_score: float = Field(..., ge=0, le=10, description="Score from the Pitch Strength Agent (0-10)")
    identity_model_score: float = Field(..., ge=0, le=10, description="Score from the Identity Model Agent (0-10)")
    momentum_tracker_score: float = Field(..., ge=0, le=10, description="Score from the Momentum Tracker Agent (0-10)")

    class Config:
        # This provides a sample payload that will appear in the API docs.
        # It makes it much easier to test and understand the endpoint.
        schema_extra = {
            "example": {
                "pitch_strength_score": 8.5,
                "identity_model_score": 7.2,
                "momentum_tracker_score": 6.8
            }
        }


# --- 3. DEFINE THE OUTPUT DATA MODEL ---
# This defines the structure of the JSON response our API will send back.
class PredictionOutput(BaseModel):
    prediction_score: float
    prediction_label: str
    key_drivers: list[str]


# --- 4. CREATE THE PREDICTION ENDPOINT ---
# The decorator '@app.post("/predict")' tells FastAPI to create a POST endpoint at the URL '/predict'.
# It will automatically handle JSON parsing for inputs that match 'AgentInput'.
# The 'response_model' ensures our output matches the 'PredictionOutput' structure.
@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: AgentInput):
    """
    Accepts scores from other AI agents and returns a fundraise prediction.

    - **pitch_strength_score**: The narrative and clarity score of the project's pitch.
    - **identity_model_score**: The trust and reputation score of the founder/team.
    - **momentum_tracker_score**: The traction and community engagement score.
    """

    # --- MOCK PREDICTION LOGIC (FOR NOW) ---
    # This is a placeholder. In Day 3, we will replace this with our actual XGBoost model.
    # We are checking a simple condition to return one of two mock responses.

    if input_data.pitch_strength_score > 7:
        mock_response = {
            "prediction_score": 0.82,
            "prediction_label": "Likely to Fund",
            "key_drivers": ["High Pitch Strength", "Strong Founder Trust"]
        }
    else:
        mock_response = {
            "prediction_score": 0.34,
            "prediction_label": "Unlikely to Fund",
            "key_drivers": ["Low Pitch Strength", "Weak Momentum"]
        }

    return mock_response

# --- 5. ADD A ROOT ENDPOINT FOR HEALTH CHECKS ---
# This is a best practice. It's a simple endpoint to check if the API is running.
@app.get("/")
def read_root():
    return {"status": "ok", "agent": "Project Chimera v1.0"}
