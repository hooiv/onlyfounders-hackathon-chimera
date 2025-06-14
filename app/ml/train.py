import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os

# --- 1. SETTINGS ---
# Define the path where the model will be saved.
# os.path.join ensures it works on any operating system.
MODEL_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(MODEL_DIR, "predictor.bst")
NUM_SAMPLES = 1000  # The number of mock data points to generate.

def generate_mock_data(num_samples: int) -> pd.DataFrame:
    """
    Generates a DataFrame with mock data representing startup agent scores.
    The logic is designed to create plausible correlations between scores and success.
    """
    print(f"Generating {num_samples} mock data samples...")

    # Generate base scores from a uniform distribution (0-10)
    data = {
        "pitch_strength_score": np.random.uniform(1, 10, num_samples),
        "identity_model_score": np.random.uniform(1, 10, num_samples),
        "momentum_tracker_score": np.random.uniform(1, 10, num_samples),
    }
    df = pd.DataFrame(data)

    # --- Create a plausible "success" condition ---
    # Success is more likely if the *average* score is high, with some randomness.
    # We add noise to make the prediction task non-trivial for the model.
    # The threshold (6.0) is arbitrary but creates a reasonably balanced dataset.
    success_probability = df.mean(axis=1) / 10 # Normalize avg score to be between 0 and 1

    # Introduce non-linearity: strong pitches matter more
    success_probability += (df['pitch_strength_score'] / 10) * 0.2

    # Add random noise to make it realistic
    noise = np.random.normal(0, 0.1, num_samples)
    final_probability = np.clip(success_probability + noise, 0, 1)

    # Create the binary target variable 'will_fund' (1 for success, 0 for failure)
    df['will_fund'] = (final_probability > 0.65).astype(int)

    print("Mock data generated. Class distribution:")
    print(df['will_fund'].value_counts(normalize=True))

    return df

def train_model():
    """
    Main function to orchestrate data generation, model training, and saving.
    """
    # Generate the data
    df = generate_mock_data(NUM_SAMPLES)

    # Define features (X) and target (y)
    features = ["pitch_strength_score", "identity_model_score", "momentum_tracker_score"]
    target = "will_fund"

    X = df[features]
    y = df[target]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # --- Initialize and train the XGBoost Classifier ---
    # These are standard, robust parameters for XGBoost.
    print("\nTraining XGBoost model...")
    xgb_classifier = xgb.XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss',
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        use_label_encoder=False,
        random_state=42
    )

    xgb_classifier.fit(X_train, y_train)
    print("Model training complete.")

    # --- Evaluate the model on the test set ---
    print("\nEvaluating model performance...")
    y_pred = xgb_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Set Accuracy: {accuracy * 100:.2f}%")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # --- Save the trained model ---
    print(f"\nSaving model to: {MODEL_PATH}")
    xgb_classifier.save_model(MODEL_PATH)
    print("Model saved successfully.")


if __name__ == "__main__":
    # This block ensures the training process runs only when the script is executed directly.
    train_model()
