import gradio as gr
import requests # The library to make HTTP requests to our API
import json

# --- 1. CONFIGURATION ---
# Define the URL of your running FastAPI backend.
# If you are running both locally, this is the default.
API_URL = "http://127.0.0.1:8000/predict"


# --- 2. THE CORE FUNCTION ---
# This function will be called every time the user interacts with the UI.
def get_prediction(pitch_score, identity_score, momentum_score):
    """
    Sends input data to the FastAPI backend and returns the formatted prediction.
    """
    # Create the payload (the JSON data) to send to the API.
    payload = {
        "pitch_strength_score": pitch_score,
        "identity_model_score": identity_score,
        "momentum_tracker_score": momentum_score
    }
    
    try:
        # Make the POST request to our API.
        response = requests.post(API_URL, json=payload)
        
        # Check if the request was successful.
        if response.status_code == 200:
            # Parse the JSON response from the API.
            result = response.json()
            
            # Extract the individual pieces of information.
            score = result["prediction_score"]
            label = result["prediction_label"]
            drivers = "\n".join(f"- {driver}" for driver in result["key_drivers"])

            # Format a nice output string.
            output_text = (
                f"**Prediction Score:** {score:.2f}\n"
                f"**Prediction Label:** {label}\n\n"
                f"**Key Drivers for this Prediction:**\n{drivers}"
            )
            return output_text
        else:
            # If the API returns an error, show it.
            return f"Error: Received status code {response.status_code}\n{response.text}"
            
    except requests.exceptions.ConnectionError:
        # If the API server is not running, show a helpful message.
        return "Error: Could not connect to the API. Please ensure the backend server is running."
    except Exception as e:
        # Catch any other unexpected errors.
        return f"An unexpected error occurred: {e}"


# --- 3. BUILD THE GRADIO INTERFACE ---

# Define the input components for the UI.
# We use Sliders for a great interactive experience.
inputs = [
    gr.Slider(minimum=0, maximum=10, value=8.5, step=0.1, label="Pitch Strength Score", 
              info="How strong is the project's narrative and clarity?"),
    gr.Slider(minimum=0, maximum=10, value=7.2, step=0.1, label="Founder Identity Score",
              info="How reputable and trustworthy is the founding team?"),
    gr.Slider(minimum=0, maximum=10, value=6.8, step=0.1, label="Project Momentum Score",
              info="How much traction and community engagement does the project have?")
]

# Define the output component.
# We use a Markdown component to allow for rich text formatting (like bold).
outputs = gr.Markdown(label="Prediction Result")

# Create the Gradio Interface object.
# This ties everything together: the function, inputs, and outputs.
demo = gr.Interface(
    fn=get_prediction,
    inputs=inputs,
    outputs=outputs,
    title="Project Chimera: Fundraise Prediction Agent",
    description=(
        "An interactive demo of the Fundraise Prediction Agent. "
        "This agent consumes privacy-preserving scores from other specialized agents in the OnlyFounders swarm "
        "to predict the likelihood of a successful fundraise. Adjust the sliders to see the prediction change in real-time."
    ),
    article="**Track:** Track 3 | **Hackathon:** Only Founders AI Hackathon | **Candidate:** ADITYA CHAUHAN",
    allow_flagging="never" # Disables the "Flag" button for a cleaner look.
)

# --- 4. LAUNCH THE APP ---
if __name__ == "__main__":
    print("Launching Gradio demo UI...")
    # The 'share=True' argument creates a public link, but we'll use it locally for now.
    demo.launch()
