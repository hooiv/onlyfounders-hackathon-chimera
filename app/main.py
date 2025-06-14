from fastapi import FastAPI
from pydantic import BaseModel, Field

# --- NEW: IMPORT THE PREDICTION LOGIC ---
# We are now importing our own custom module.
# This keeps the API code clean and separates concerns.
from app.model import predict_and_explain

# --- 1. DEFINE THE API ---
# No changes here.
app = FastAPI(
    title="Project Chimera: Fundraise Prediction Agent",
    version="1.0",
    description="A privacy-preserving AI agent to predict startup fundraising success."
)

# --- 2. DEFINE THE INPUT DATA MODEL ---
# No changes here.
class AgentInput(BaseModel):
    pitch_strength_score: float = Field(..., ge=0, le=10, description="Score from the Pitch Strength Agent (0-10)")
    identity_model_score: float = Field(..., ge=0, le=10, description="Score from the Identity Model Agent (0-10)")
    momentum_tracker_score: float = Field(..., ge=0, le=10, description="Score from the Momentum Tracker Agent (0-10)")

    class Config:
        schema_extra = {
            "example": {
                "pitch_strength_score": 8.5,
                "identity_model_score": 7.2,
                "momentum_tracker_score": 6.8
            }
        }

# --- 3. DEFINE THE OUTPUT DATA MODEL ---
# No changes here.
class PredictionOutput(BaseModel):
    prediction_score: float
    prediction_label: str
    key_drivers: list[str]

# --- 4. CREATE THE PREDICTION ENDPOINT ---
# This is the main change. We are replacing the mock logic with a real model call.
@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: AgentInput):
    """
    Accepts scores from other AI agents and returns a fundraise prediction.

    - **pitch_strength_score**: The narrative and clarity score of the project's pitch.
    - **identity_model_score**: The trust and reputation score of the founder/team.
    - **momentum_tracker_score**: The traction and community engagement score.
    """

    # --- REAL PREDICTION LOGIC ---
    # 1. Convert the Pydantic input model to a dictionary.
    #    The `dict()` method is a convenient way to do this.
    input_dict = input_data.dict()

    # 2. Call our imported function to get the prediction and explanation.
    #    All the complex logic is neatly hidden away in model.py.
    result = predict_and_explain(input_dict)

    # 3. Return the result. FastAPI will automatically serialize it to JSON.
    return result

# --- 5. ADD A ROOT ENDPOINT FOR HEALTH CHECKS ---
# No changes here.
@app.get("/")
def read_root():
    return {"status": "ok", "agent": "Project Chimera v1.0"}
