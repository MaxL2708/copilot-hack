# Create a base Flask server

import pickle
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure CORS to allow localhost only (for development)
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')

# Enable cors with restricted origins
@app.after_request
def after_request(response):
    """
    Enable CORS with origin restrictions
    """
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


# Load model from pickle file (only load from trusted sources)
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Model takes two parameters - day of week and airport id, then returns a prediction of flight delay
@app.route('/predict', methods=['GET'])
def predict():
    """
    Takes two parameters - day of week and airport id, then returns a prediction of flight delay
    """
    try:
        # Store day_of_week as int with validation
        day_of_week = int(request.args.get('day_of_week', 0))
        airport_id = int(request.args.get('airport_id', 0))
        
        # Validate ranges
        if not (1 <= day_of_week <= 7):
            return jsonify({'error': 'day_of_week must be between 1 and 7'}), 400
        if airport_id <= 0:
            return jsonify({'error': 'airport_id must be positive'}), 400
        
        prediction = model.predict_proba([[day_of_week, airport_id]])[0]
        
        # Split prediction string by space
        prediction = str(prediction).split(' ')

        # store first value from prediction as certainty, and remove the first character
        certainty = float(prediction[0][2:])

        # store second value from prediction as delay, and remove the last character
        delay = float(prediction[1][:-1])

        # return prediction as json
        return jsonify({'certainty': certainty, 'delay': delay})
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input parameters'}), 400
    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500

# Create a new route called airports with method of get
@app.route('/airports', methods=['GET'])
def airports():
    # Load airports from csv file
    airports = open('airports.csv', 'r').readlines()

    # Remove first line of airports
    airports.pop(0)

    # Create list with dictionary of airports
    # First value is id, second is name
    # Convert id to integer
    # Remove last character from name
    airports = [{'id': int(airport.split(',')[0]), 'name': airport.split(',')[1][:-1]} for airport in airports]
    # Sort by name
    airports = sorted(airports, key=lambda k: k['name'])

    return jsonify(airports)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
