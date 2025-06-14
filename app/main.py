"""
Project Chimera - FastAPI Server
Track 3: Fundraise Prediction Agent

This module contains the main FastAPI application for the fundraise prediction agent.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn

app = FastAPI(
    title="Project Chimera - Fundraise Prediction Agent",
    description="Privacy-preserving fundraise prediction agent for OnlyFounders AI swarm",
    version="1.0.0"
)

class PredictionInput(BaseModel):
    """Input model for prediction requests"""
    pitch_score: float
    trust_score: float
    momentum_score: float

class PredictionOutput(BaseModel):
    """Output model for prediction responses"""
    prediction_score: float
    prediction_label: str
    key_drivers: List[str]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Project Chimera - Fundraise Prediction Agent is running"}

@app.post("/predict", response_model=PredictionOutput)
async def predict_fundraise(input_data: PredictionInput):
    """
    Main prediction endpoint
    
    Takes privacy-preserving scores from other agents and returns
    an explainable fundraise prediction.
    """
    # TODO: Implement actual prediction logic
    # This is a placeholder implementation
    
    # Simple weighted average for now
    weighted_score = (
        input_data.pitch_score * 0.4 +
        input_data.trust_score * 0.35 +
        input_data.momentum_score * 0.25
    ) / 10.0  # Normalize to 0-1 range
    
    # Determine label
    if weighted_score >= 0.7:
        label = "Likely to Fund"
    elif weighted_score >= 0.5:
        label = "Moderate Potential"
    else:
        label = "Low Funding Probability"
    
    # Simple key drivers logic
    scores = {
        "pitch_score": input_data.pitch_score,
        "trust_score": input_data.trust_score,
        "momentum_score": input_data.momentum_score
    }
    
    # Find top 2 drivers
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    key_drivers = []
    
    if sorted_scores[0][0] == "pitch_score":
        key_drivers.append("High Pitch Strength" if sorted_scores[0][1] >= 7 else "Moderate Pitch Strength")
    elif sorted_scores[0][0] == "trust_score":
        key_drivers.append("Strong Founder Trust" if sorted_scores[0][1] >= 7 else "Moderate Founder Trust")
    else:
        key_drivers.append("Strong Momentum" if sorted_scores[0][1] >= 7 else "Moderate Momentum")
    
    if sorted_scores[1][0] == "pitch_score":
        key_drivers.append("Pitch Quality" if sorted_scores[1][1] >= 6 else "Pitch Needs Improvement")
    elif sorted_scores[1][0] == "trust_score":
        key_drivers.append("Founder Credibility" if sorted_scores[1][1] >= 6 else "Trust Building Needed")
    else:
        key_drivers.append("Market Traction" if sorted_scores[1][1] >= 6 else "Limited Traction")
    
    return PredictionOutput(
        prediction_score=round(weighted_score, 2),
        prediction_label=label,
        key_drivers=key_drivers[:2]
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
