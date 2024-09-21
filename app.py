from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, jsonify
import json
from fuzzywuzzy import process
from symptom_checker import *

app = Flask(__name__)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)


def load_data():
    with open('pet_symptoms.json', 'r') as file:
        return json.load(file)

@app.route('/check', methods=['POST'])
def check_symptoms():
    data = load_data()
    pet_type = request.json.get('pet_type').lower()
    symptoms = request.json.get('symptoms', [])  # Get the array of symptoms
    all_conditions = []
    severity = None
    action = None
    
    for symptom in symptoms:
        if symptom in data[pet_type]["symptoms"]:
            conditions_info = data[pet_type]["symptoms"][symptom]
            all_conditions.extend(conditions_info["conditions"])
            severity = conditions_info["severity"]  # You might want to handle multiple severities
            action = conditions_info["action"]  # Similar handling for actions

    return jsonify({'conditions': all_conditions, 'severity': severity, 'action': action})


if __name__ == "__main__":
    app.run(debug=True)
