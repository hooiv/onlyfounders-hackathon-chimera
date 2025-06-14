import xgboost as xgb
import pandas as pd
import shap
import os

# --- 1. LOAD THE MODEL AND EXPLAINER ON STARTUP ---

# Define the path to the model file.
# This makes the code robust to where you run it from.
MODEL_DIR = os.path.join(os.path.dirname(__file__), "ml")
MODEL_PATH = os.path.join(MODEL_DIR, "predictor.bst")

# Load the XGBoost model from the file.
# This is done once when the application starts, making predictions faster.
print(f"Loading model from: {MODEL_PATH}")
model = xgb.Booster()
model.load_model(MODEL_PATH)
print("Model loaded successfully.")

# Create a SHAP explainer object.
# This is used to understand the "why" behind each prediction.
# Like the model, it's loaded once for efficiency.
explainer = shap.TreeExplainer(model)
print("SHAP explainer created.")

# Define the feature names in the exact order the model was trained on.
# This is CRITICAL for both prediction and explanation.
feature_names = ["pitch_strength_score", "identity_model_score", "momentum_tracker_score"]


def predict_and_explain(input_data: dict) -> dict:
    """
    Takes a dictionary of input scores, makes a prediction, and explains it.

    Args:
        input_data (dict): A dictionary with keys matching the feature_names.

    Returns:
        dict: A dictionary containing the prediction, label, and key drivers.
    """
    # --- 1. PREPARE THE INPUT ---
    # Convert the input dictionary to a pandas DataFrame.
    # The model expects a 2D array, so we wrap it in a list.
    # Ensure the columns are in the same order as during training.
    input_df = pd.DataFrame([input_data])[feature_names]

    # --- 2. MAKE PREDICTION ---
    # Convert the DataFrame to a DMatrix, XGBoost's internal data structure.
    dmatrix = xgb.DMatrix(input_df)

    # Use the model to predict the probability of success (funding).
    # The output is a probability score between 0 and 1.
    prediction_score = model.predict(dmatrix)[0]

    # Convert the numerical score to a human-readable label.
    prediction_label = "Likely to Fund" if prediction_score > 0.5 else "Unlikely to Fund"

    # --- 3. EXPLAIN THE PREDICTION ---
    # Use the SHAP explainer to calculate Shapley values for this specific prediction.
    # Shapley values show the contribution of each feature to the final prediction.
    shap_values = explainer.shap_values(input_df)

    # Associate feature names with their SHAP values.
    feature_impact = dict(zip(feature_names, shap_values[0]))

    # Sort features by the absolute magnitude of their impact.
    # This tells us which features were most influential.
    sorted_drivers = sorted(feature_impact.items(), key=lambda item: abs(item[1]), reverse=True)

    # Format the key drivers for a clean API response.
    # We'll just take the top 2 most influential features.
    key_drivers = [f"Impact of {name.replace('_', ' ').title()}" for name, impact in sorted_drivers[:2]]

    # --- 4. FORMAT THE OUTPUT ---
    # Bundle everything into a structured dictionary for the API to return.
    result = {
        "prediction_score": float(prediction_score),
        "prediction_label": prediction_label,
        "key_drivers": key_drivers
    }

    return result
