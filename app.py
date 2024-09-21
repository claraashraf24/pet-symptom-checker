from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, jsonify
import json
from fuzzywuzzy import process
from symptom_checker import *

app = Flask(__name__)

def load_data():
    with open('pet_symptoms.json', 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/check', methods=['POST'])
def check_symptoms():
    data = load_data()
    pet_type = request.json.get('pet_type').lower()
    symptom = request.json.get('symptom').lower()
    common_symptoms = data.get(pet_type, {}).get("common_symptoms", [])
    
    # Get conditions based on the selected symptom
    if symptom in data[pet_type]["symptoms"]:
        conditions_info = data[pet_type]["symptoms"][symptom]
        conditions = conditions_info["conditions"]
        severity = conditions_info["severity"]
        action = conditions_info["action"]
        return jsonify({'conditions': conditions, 'severity': severity, 'action': action})
    else:
        return jsonify({'error': 'No data available for the given symptom.'})


if __name__ == "__main__":
    app.run(debug=True)
