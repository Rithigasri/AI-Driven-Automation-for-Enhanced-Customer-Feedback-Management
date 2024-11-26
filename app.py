from flask import Flask, request, jsonify
from transformers import pipeline
import pandas as pd
import os
import requests  # Importing requests for making API calls

# Load the pre-trained sentiment analysis model
sentiment_analysis = pipeline("sentiment-analysis")

# Initialize the Flask application
app = Flask(_name_)

# Initialize Label Studio API configuration
LABEL_STUDIO_URL = 'http://localhost:8081'  # Adjust if hosted elsewhere
API_KEY = '7cc99b8ef615ff863021715db0f0faf275522509'  # Replace with your API key
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    # Process the data as needed
    # Example: Log the sentiment information
    print(f"Task ID: {data.get('task_id')} annotated successfully with sentiment: {data.get('sentiment')}")
    return jsonify({"status": "success"}), 200
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify if the service is running."""
    return jsonify({'status': 'healthy'}), 200

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """Setup endpoint for Label Studio to verify the ML backend setup."""
    return jsonify({
        "model": "sentiment-analysis",
        "version": "1.0.0",
        "description": "Sentiment analysis model using Hugging Face Transformers."
    }), 200

def create_annotation(task_id, sentiment):
    """Create annotations in Label Studio for a given task using the REST API."""
    annotation_data = {
        "result": [
            {
                "from_name": "sentiment",
                "to_name": "text",
                "type": "choices",
                "value": {
                    "choices": [sentiment]
                }
            }
        ],
        "was_cancelled": False,
        "ground_truth": False  # Adjust this as needed
    }

    # Making a POST request to create an annotation
    response = requests.post(
        f"{LABEL_STUDIO_URL}/api/tasks/{task_id}/annotations/",
        headers={
            "Authorization": f"Token {API_KEY}",
            "Content-Type": "application/json"
        },
        json=annotation_data
    )

    if response.status_code == 201:
        print(f"Task ID {task_id} annotated successfully with sentiment: {sentiment}")
    else:
        print(f"Error annotating Task ID {task_id}: {response.text}")

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint to predict sentiment from provided review titles."""
    # Get the input data from the request
    data = request.json
    print("Received data:", data)  # Log incoming request data for debugging

    # Ensure 'tasks' key exists in the JSON body
    if 'tasks' not in data:
        return jsonify({'error': 'No tasks key found in the request.'}), 400

    # Define file path for the CSV
    csv_file_path = os.path.join(os.getcwd(), "sentiment_analysis_results.csv")

    # Process each task
    records = []
    predictions = []
    for task in data['tasks']:
        task_id = task['id']
        review_title = task['data'].get('Review Title')
        if not review_title:
            continue  # Skip tasks without a Review Title

        # Run sentiment analysis
        result = sentiment_analysis(review_title)[0]
        sentiment = result['label'].upper()  # Label for "POSITIVE," "NEGATIVE," or "NEUTRAL"
        score = result['score']

        # Add to records for CSV
        records.append({
            'Task ID': task_id,
            'Review Title': review_title,
            'Sentiment': sentiment,
            'Score': score
        })

        # Create prediction structure for Label Studio response
        prediction = {
            "model_version": "1.0.0",
            "result": [
                {
                    "id": str(task_id),
                    "from_name": "sentiment",
                    "to_name": "text",
                    "type": "choices",
                    "value": {
                        "choices": [sentiment]
                    }
                }
            ],
            "score": score
        }
        predictions.append(prediction)

        # Annotate the task in Label Studio using the REST API
        create_annotation(task_id, sentiment)

    # Append the records to the CSV file
    df = pd.DataFrame(records)
    if os.path.exists(csv_file_path):
        # Append to existing CSV
        df.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        # Create a new CSV file with headers
        df.to_csv(csv_file_path, index=False)

    # Format the response for Label Studio
    response = {"predictions": predictions}
    print("Response data:", response)  # Log the outgoing response for debugging

    return jsonify(response)

if _name_ == '_main_':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000)
